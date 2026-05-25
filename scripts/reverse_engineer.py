#!/usr/bin/env python3
"""
Reverse Engineering Engine — Library of Alexander
Distributed across the swarm. Uses spare SSD, cleans up after itself.
"""

import os
import re
import json
import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone

# ── Load config ─────────────────────────────────────────────────
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    NODE, NODE_STORAGE, NODE_RATE, get_re_targets,
    cleanup_scratch, get_scratch_usage_gb,
)

CLONE_DIR = NODE_STORAGE["clones"]
ANALYSIS_DIR = NODE_STORAGE["analysis"]
REPORTS_DIR = NODE_STORAGE["reports"]
DATA_DIR = NODE_STORAGE["data"]

for d in [CLONE_DIR, ANALYSIS_DIR, REPORTS_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def clone_repo(full_name: str) -> Path | None:
    """Clone a repo to the spare SSD scratch space."""
    dest = CLONE_DIR / full_name.replace("/", "_")
    if dest.exists():
        return dest  # Already cloned

    url = f"https://github.com/{full_name}.git"
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none",
             "--sparse", url, str(dest)],
            capture_output=True, text=True,
            timeout=NODE_RATE["clone_timeout_seconds"],
        )
        if result.returncode == 0:
            print(f"  📦 Cloned {full_name}")
            return dest
        else:
            print(f"  ❌ Clone failed: {result.stderr[:100]}")
    except subprocess.TimeoutExpired:
        print(f"  ⏰ Clone timeout for {full_name}")
    except Exception as e:
        print(f"  ❌ Clone error: {e}")
    return None


def analyze_structure(repo_path: Path) -> dict:
    """Analyze directory structure."""
    structure = {"files": [], "dirs": [], "languages": {}, "total_files": 0}
    skip = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox", "dist", "build"}

    try:
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in skip]
            for f in files:
                fp = Path(root) / f
                rel = str(fp.relative_to(repo_path))
                structure["files"].append(rel)
                structure["total_files"] += 1
                ext = Path(f).suffix
                if ext:
                    structure["languages"][ext] = structure["languages"].get(ext, 0) + 1
            for d in dirs:
                structure["dirs"].append(str((Path(root) / d).relative_to(repo_path)))
    except Exception as e:
        print(f"  Structure error: {e}")

    return structure


def analyze_code_quality(repo_path: Path) -> dict:
    """Basic code quality metrics."""
    q = {
        "has_tests": False, "has_ci": False, "has_license": False,
        "has_docs": False, "has_security_policy": False,
        "has_contributing": False, "has_readme": False,
        "readme_length": 0, "python_files": 0, "test_files": 0,
        "max_file_lines": 0, "avg_file_lines": 0,
        "has_type_hints": False, "has_docker": False,
        "has_makefile": False, "has_precommit": False,
    }

    try:
        q["has_license"] = any((repo_path / f).exists() for f in
            ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE-MIT"])
        q["has_contributing"] = any((repo_path / f).exists() for f in
            ["CONTRIBUTING.md", "CONTRIBUTING.rst"])
        q["has_security_policy"] = (repo_path / "SECURITY.md").exists()
        q["has_readme"] = any((repo_path / f).exists() for f in
            ["README.md", "README.rst", "README"])
        q["has_ci"] = (repo_path / ".github").is_dir() or (repo_path / ".travis.yml").exists()
        q["has_docs"] = any((repo_path / d).is_dir() for d in ["docs", "doc", "documentation"])
        q["has_docker"] = any((repo_path / f).exists() for f in
            ["Dockerfile", "docker-compose.yml"])
        q["has_makefile"] = (repo_path / "Makefile").exists()
        q["has_precommit"] = (repo_path / ".pre-commit-config.yaml").exists()
        q["has_tests"] = any((repo_path / d).is_dir() for d in
            ["tests", "test", "__tests__", "spec"])

        py_lines = []
        for f in repo_path.rglob("*.py"):
            if ".git" in str(f) or "__pycache__" in str(f):
                continue
            try:
                content = f.read_text(errors="ignore")
                n = len(content.splitlines())
                py_lines.append(n)
                if "def " in content and "->" in content:
                    q["has_type_hints"] = True
                if "test_" in f.name or "tests" in str(f.parent):
                    q["test_files"] += 1
            except:
                pass

        q["python_files"] = len(py_lines)
        q["max_file_lines"] = max(py_lines) if py_lines else 0
        q["avg_file_lines"] = sum(py_lines) // len(py_lines) if py_lines else 0

        for readme in ["README.md", "README.rst", "README"]:
            rp = repo_path / readme
            if rp.exists():
                try:
                    q["readme_length"] = len(rp.read_text(errors="ignore").splitlines())
                except:
                    pass
                break
    except Exception as e:
        print(f"  Quality error: {e}")

    return q


def extract_architecture(repo_path: Path) -> dict:
    """Extract architecture info from source files."""
    arch = {"classes": [], "functions": [], "imports": [], "patterns": []}

    try:
        all_content = ""
        for f in list(repo_path.rglob("*.py"))[:30]:
            if ".git" in str(f) or "__pycache__" in str(f):
                continue
            try:
                content = f.read_text(errors="ignore")
                arch["classes"].extend(re.findall(r'^class\s+(\w+)', content, re.MULTILINE)[:10])
                arch["functions"].extend(re.findall(r'^def\s+(\w+)', content, re.MULTILINE)[:10])
                arch["imports"].extend(re.findall(r'^(?:from|import)\s+(\w+)', content, re.MULTILINE)[:15])
                all_content += content[:5000]
            except:
                pass

        arch["classes"] = list(dict.fromkeys(arch["classes"]))[:40]
        arch["functions"] = list(dict.fromkeys(arch["functions"]))[:40]
        arch["imports"] = list(dict.fromkeys(arch["imports"]))[:40]

        # Detect patterns
        checks = [
            ("Agent-Tool", "Agent" in all_content and "Tool" in all_content),
            ("Chain pattern", "Chain" in all_content),
            ("RAG pattern", "retrieval" in all_content.lower() or "RAG" in all_content),
            ("ReAct reasoning", "ReAct" in all_content or "Thought" in all_content),
            ("MCP integration", "MCP" in all_content or "Model Context Protocol" in all_content),
            ("Async/await", "async " in all_content and "await " in all_content),
            ("Pydantic models", "pydantic" in all_content or "BaseModel" in all_content),
            ("Web API", "fastapi" in all_content or "Flask" in all_content),
            ("Web UI", "streamlit" in all_content or "gradio" in all_content),
        ]
        arch["patterns"] = [name for name, check in checks if check]
    except Exception as e:
        print(f"  Arch error: {e}")

    return arch


def generate_report(full_name, structure, quality, arch) -> str:
    """Generate markdown report."""
    score = sum([
        1 if quality["has_license"] else 0,
        2 if quality["has_tests"] else 0,
        1 if quality["has_ci"] else 0,
        1 if quality["has_docs"] else 0,
        1 if quality["has_type_hints"] else 0,
        1 if quality["has_docker"] else 0,
        1 if quality["max_file_lines"] < 500 else 0,
        2 if quality["test_files"] > 5 else 0,
        1 if quality["readme_length"] > 100 else 0,
    ])

    verdict = "🟢 High Quality" if score >= 8 else "🟡 Medium Quality" if score >= 5 else "🔴 Low Quality (likely vibe-coded)"

    lines = [
        f"# 🔬 Reverse Engineering: {full_name}",
        f"",
        f"> Node: {NODE} | Auto-generated by Library of Alexander",
        f"",
        f"## Overview",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Files | {structure['total_files']} |",
        f"| Python Files | {quality['python_files']} |",
        f"| Test Files | {quality['test_files']} |",
        f"| Max File Lines | {quality['max_file_lines']} |",
        f"| Avg File Lines | {quality['avg_file_lines']} |",
        f"| README Length | {quality['readme_length']} lines |",
        f"",
        f"## Quality Checklist",
        f"",
        f"| Check | Status |",
        f"|-------|--------|",
        f"| License | {'✅' if quality['has_license'] else '❌'} |",
        f"| Tests | {'✅' if quality['has_tests'] else '❌'} |",
        f"| CI/CD | {'✅' if quality['has_ci'] else '❌'} |",
        f"| Documentation | {'✅' if quality['has_docs'] else '❌'} |",
        f"| Contributing Guide | {'✅' if quality['has_contributing'] else '❌'} |",
        f"| Docker | {'✅' if quality['has_docker'] else '❌'} |",
        f"| Makefile | {'✅' if quality['has_makefile'] else '❌'} |",
        f"| Type Hints | {'✅' if quality['has_type_hints'] else '❌'} |",
        f"",
        f"## Architecture Patterns",
        f"",
    ]
    lines.extend(f"- {p}" for p in arch["patterns"]) if arch["patterns"] else lines.append("No patterns detected")
    lines += [
        f"",
        f"## Key Classes",
        f"",
    ]
    lines.extend(f"- `{c}`" for c in arch["classes"][:20]) if arch["classes"] else lines.append("None detected")
    lines += [
        f"",
        f"## Key Functions",
        f"",
    ]
    lines.extend(f"- `{f}`" for f in arch["functions"][:20]) if arch["functions"] else lines.append("None detected")
    lines += [
        f"",
        f"## Verdict",
        f"",
        f"**{verdict}** — Quality Score: **{score}/10**",
        f"",
        f"---",
        f"*Generated: {datetime.now(timezone.utc).isoformat()} UTC on {NODE}*",
    ]

    return "\n".join(lines)


def delete_clone(repo_path: Path):
    """Delete cloned repo from scratch space after analysis."""
    try:
        shutil.rmtree(repo_path, ignore_errors=True)
        print(f"  🗑️ Deleted clone: {repo_path.name}")
    except Exception as e:
        print(f"  ⚠️ Cleanup error: {e}")


def main():
    targets = get_re_targets()
    print(f"🔬 Reverse Engineering Engine — Node: {NODE}")
    print(f"Time: {datetime.now(timezone.utc).isoformat()} UTC")
    print(f"Targets: {len(targets)} repos")
    print(f"Scratch: {NODE_STORAGE['scratch']} (max {NODE_STORAGE['max_scratch_gb']}GB)")
    print(f"Scratch usage: {get_scratch_usage_gb(NODE_STORAGE['scratch']):.1f}GB")
    print()

    # Clean up before starting
    cleanup_scratch(NODE_STORAGE)

    results = []

    for full_name in targets:
        print(f"\n=== {full_name} ===")

        # Clone to spare SSD
        repo_path = clone_repo(full_name)
        if not repo_path:
            continue

        # Analyze
        structure = analyze_structure(repo_path)
        quality = analyze_code_quality(repo_path)
        arch = extract_architecture(repo_path)

        # Generate report
        report = generate_report(full_name, structure, quality, arch)

        # Save report to the knowledge base (not scratch)
        safe_name = full_name.replace("/", "_")
        report_path = REPORTS_DIR / f"RE_{safe_name}.md"
        report_path.write_text(report)
        print(f"  📝 Report: {report_path.name}")

        # Save analysis data
        analysis_path = ANALYSIS_DIR / f"{safe_name}.json"
        analysis_path.write_text(json.dumps({
            "repo": full_name,
            "node": NODE,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "structure": {k: v for k, v in structure.items() if k != "files"},
            "quality": quality,
            "arch": arch,
            "score": sum([
                1 if quality["has_license"] else 0,
                2 if quality["has_tests"] else 0,
                1 if quality["has_ci"] else 0,
                1 if quality["has_docs"] else 0,
                1 if quality["has_type_hints"] else 0,
                1 if quality["has_docker"] else 0,
                1 if quality["max_file_lines"] < 500 else 0,
                2 if quality["test_files"] > 5 else 0,
                1 if quality["readme_length"] > 100 else 0,
            ]),
        }, indent=2))

        results.append({"repo": full_name, "score": sum([
            1 if quality["has_license"] else 0,
            2 if quality["has_tests"] else 0,
            1 if quality["has_ci"] else 0,
            1 if quality["has_docs"] else 0,
            1 if quality["has_type_hints"] else 0,
            1 if quality["has_docker"] else 0,
            1 if quality["max_file_lines"] < 500 else 0,
            2 if quality["test_files"] > 5 else 0,
            1 if quality["readme_length"] > 100 else 0,
        ])})

        # DELETE CLONE immediately after analysis — don't fill the SSD
        delete_clone(repo_path)

        # Pause between clones
        time.sleep(NODE_RATE["github_api_pause_seconds"])

    # Final cleanup
    cleanup_scratch(NODE_STORAGE)

    # Save summary
    summary = {
        "node": NODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }
    summary_path = DATA_DIR / f"re_summary_{NODE}.json"
    summary_path.write_text(json.dumps(summary, indent=2))

    # Print summary
    print(f"\n{'='*60}")
    print(f"✅ RE complete on {NODE}. {len(results)} repos analyzed.")
    print(f"Scratch usage: {get_scratch_usage_gb(NODE_STORAGE['scratch']):.1f}GB")
    print(f"\nQuality Rankings:")
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        v = "🟢" if r["score"] >= 8 else "🟡" if r["score"] >= 5 else "🔴"
        print(f"  {v} {r['repo']}: {r['score']}/10")


if __name__ == "__main__":
    main()
