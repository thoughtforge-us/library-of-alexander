#!/usr/bin/env python3
"""
Library of Alexander — Main Pipeline
Scrapes GitHub → Reverse Engineers → Pushes to Git
Runs continuously. Push every 4h. Clean scratch every 5h.
"""

import os, re, json, shutil, subprocess, time, sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    NODE, S, GITHUB_QUERIES, CHINESE_ORGS, WESTERN_ORGS,
    get_re_targets, scratch_usage_gb, cleanup_scratch,
)

REPO_ROOT = Path(__file__).parent.parent
CLONES = S["clones"]
ANALYSIS = S["analysis"]
REPORTS = S["reports"]
DATA = S["data"]

# ── GitHub Scraping ─────────────────────────────────────────────
def gh_api(path):
    """Call GitHub API via gh CLI."""
    try:
        r = subprocess.run(
            ["gh", "api", path, "--paginate"],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode == 0:
            return json.loads(r.stdout)
    except:
        pass
    return None


def scrape_org(org):
    """Scrape all repos from an org."""
    repos = []
    data = gh_api(f"orgs/{org}/repos?per_page=100&sort=stars&direction=desc")
    if isinstance(data, list):
        for r in data:
            repos.append({
                "full_name": r.get("full_name", ""),
                "description": (r.get("description") or "")[:100],
                "url": r.get("html_url", ""),
                "language": r.get("language"),
                "stars": r.get("stargazers_count", 0),
                "topics": r.get("topics", []),
                "license": r.get("license", {}).get("spdx_id") if r.get("license") else None,
                "updated": r.get("updated_at", ""),
            })
    return repos


def scrape_search(query, limit=30):
    """Search GitHub for repos."""
    repos = []
    try:
        r = subprocess.run(
            ["gh", "search", "repos", query, "--sort", "stars",
             "--limit", str(limit), "--json",
             "fullName,stargazersCount,description,language,url,license,topics"],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode == 0:
            data = json.loads(r.stdout)
            for item in data:
                repos.append({
                    "full_name": item.get("fullName", ""),
                    "description": (item.get("description") or "")[:100],
                    "url": item.get("url", ""),
                    "language": item.get("language"),
                    "stars": item.get("stargazersCount", 0),
                    "topics": item.get("topics", []),
                    "license": item.get("license"),
                })
    except:
        pass
    return repos


def scrape_all():
    """Scrape everything — orgs + searches."""
    print(f"🔍 Scraping GitHub on {NODE}...")
    all_repos = {}
    seen = set()

    # 1. Scrape orgs
    all_orgs = CHINESE_ORGS + WESTERN_ORGS
    for org in all_orgs:
        repos = scrape_org(org)
        for r in repos:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                all_repos[r["full_name"]] = r
        print(f"  {org}: {len(repos)} repos")
        time.sleep(1)

    # 2. Scrape search queries
    for category, query in GITHUB_QUERIES.items():
        repos = scrape_search(query, limit=20)
        new = 0
        for r in repos:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                all_repos[r["full_name"]] = r
                new += 1
        print(f"  {category}: {new} new repos")
        time.sleep(2)

    print(f"✅ Scraped {len(all_repos)} unique repos")
    return list(all_repos.values())


# ── Reverse Engineering ────────────────────────────────────────
def clone_repo(full_name):
    """Clone repo to scratch SSD."""
    dest = CLONES / full_name.replace("/", "_")
    if dest.exists():
        return dest
    url = f"https://github.com/{full_name}.git"
    try:
        r = subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none",
             "--sparse", url, str(dest)],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode == 0:
            return dest
    except:
        pass
    return None


def analyze_repo(repo_path):
    """Analyze a cloned repo. Returns quality metrics."""
    q = {
        "total_files": 0, "python_files": 0, "test_files": 0,
        "max_lines": 0, "avg_lines": 0, "languages": {},
        "has_license": False, "has_tests": False, "has_ci": False,
        "has_docs": False, "has_docker": False, "has_type_hints": False,
        "readme_lines": 0, "classes": [], "functions": [],
        "patterns": [],
    }
    skip = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".tox"}
    py_lines = []

    try:
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in skip]
            for f in files:
                fp = Path(root) / f
                q["total_files"] += 1
                ext = Path(f).suffix
                if ext:
                    q["languages"][ext] = q["languages"].get(ext, 0) + 1
                if ext == ".py":
                    try:
                        content = fp.read_text(errors="ignore")
                        n = len(content.splitlines())
                        py_lines.append(n)
                        if "def " in content and "->" in content:
                            q["has_type_hints"] = True
                        if "test_" in f or "tests" in str(fp.parent):
                            q["test_files"] += 1
                        q["classes"].extend(re.findall(r'^class\s+(\w+)', content, re.MULTILINE)[:5])
                        q["functions"].extend(re.findall(r'^def\s+(\w+)', content, re.MULTILINE)[:5])
                    except:
                        pass

        q["python_files"] = len(py_lines)
        q["max_lines"] = max(py_lines) if py_lines else 0
        q["avg_lines"] = sum(py_lines) // len(py_lines) if py_lines else 0

        q["has_license"] = any((repo_path / f).exists() for f in ["LICENSE", "LICENSE.md", "LICENSE.txt"])
        q["has_tests"] = any((repo_path / d).is_dir() for d in ["tests", "test", "__tests__"])
        q["has_ci"] = (repo_path / ".github").is_dir()
        q["has_docs"] = any((repo_path / d).is_dir() for d in ["docs", "doc"])
        q["has_docker"] = (repo_path / "Dockerfile").exists()

        for readme in ["README.md", "README.rst", "README"]:
            rp = repo_path / readme
            if rp.exists():
                q["readme_lines"] = len(rp.read_text(errors="ignore").splitlines())
                break

        # Detect patterns
        sample = ""
        for f in list(repo_path.rglob("*.py"))[:20]:
            try: sample += f.read_text(errors="ignore")[:3000]
            except: pass
        checks = [
            ("Agent-Tool", "Agent" in sample and "Tool" in sample),
            ("Chain", "Chain" in sample),
            ("RAG", "retrieval" in sample.lower()),
            ("ReAct", "ReAct" in sample or "Thought" in sample),
            ("MCP", "MCP" in sample),
            ("Async", "async " in sample and "await " in sample),
            ("Pydantic", "pydantic" in sample or "BaseModel" in sample),
            ("FastAPI", "fastapi" in sample),
            ("WebUI", "streamlit" in sample or "gradio" in sample),
        ]
        q["patterns"] = [n for n, c in checks if c]
        q["classes"] = list(dict.fromkeys(q["classes"]))[:30]
        q["functions"] = list(dict.fromkeys(q["functions"]))[:30]

    except Exception as e:
        print(f"  Analysis error: {e}")

    return q


def score_quality(q):
    """Score 0-10."""
    return sum([
        1 if q["has_license"] else 0,
        2 if q["has_tests"] else 0,
        1 if q["has_ci"] else 0,
        1 if q["has_docs"] else 0,
        1 if q["has_type_hints"] else 0,
        1 if q["has_docker"] else 0,
        1 if q["max_lines"] < 500 else 0,
        2 if q["test_files"] > 5 else 0,
        1 if q["readme_lines"] > 100 else 0,
    ])


def reverse_engineer(repos):
    """Clone, analyze, report, delete. Returns list of results."""
    print(f"🔬 Reverse engineering {len(repos)} repos on {NODE}...")
    results = []

    for repo in repos:
        full_name = repo["full_name"]
        print(f"  {full_name}...", end=" ", flush=True)

        repo_path = clone_repo(full_name)
        if not repo_path:
            print("SKIP (clone failed)")
            continue

        q = analyze_repo(repo_path)
        score = score_quality(q)
        verdict = "🟢" if score >= 8 else "🟡" if score >= 5 else "🔴"

        # Save report to git-tracked directory
        safe = full_name.replace("/", "_")
        report_path = REPO_ROOT / "23-reverse-engineering" / f"RE_{safe}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# 🔬 RE: {full_name}",
            f"> Node: {NODE} | {datetime.now(timezone.utc).isoformat()} UTC",
            f"",
            f"## Quality: {verdict} {score}/10",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Files | {q['total_files']} |",
            f"| Python Files | {q['python_files']} |",
            f"| Test Files | {q['test_files']} |",
            f"| Max Lines | {q['max_lines']} |",
            f"| Avg Lines | {q['avg_lines']} |",
            f"| README | {q['readme_lines']} lines |",
            f"| License | {'✅' if q['has_license'] else '❌'} |",
            f"| Tests | {'✅' if q['has_tests'] else '❌'} |",
            f"| CI/CD | {'✅' if q['has_ci'] else '❌'} |",
            f"| Docker | {'✅' if q['has_docker'] else '❌'} |",
            f"| Type Hints | {'✅' if q['has_type_hints'] else '❌'} |",
            f"",
            f"## Patterns",
        ]
        lines += [f"- {p}" for p in q["patterns"]] if q["patterns"] else ["None detected"]
        lines += ["", "## Key Classes"]
        lines += [f"- `{c}`" for c in q["classes"][:15]] if q["classes"] else ["None"]
        lines += ["", "## Key Functions"]
        lines += [f"- `{f}`" for f in q["functions"][:15]] if q["functions"] else ["None"]
        lines += ["", "## Languages"]
        for ext, count in sorted(q["languages"].items(), key=lambda x: x[1], reverse=True)[:10]:
            lines += [f"| {ext} | {count} |"]

        report_path.write_text("\n".join(lines))

        # Save JSON data
        json_path = ANALYSIS / f"{safe}.json"
        json_path.write_text(json.dumps({
            "repo": full_name, "node": NODE, "score": score,
            "quality": {k: v for k, v in q.items() if k not in ("classes", "functions", "patterns", "languages")},
            "patterns": q["patterns"],
        }, indent=2))

        results.append({"repo": full_name, "score": score, "stars": repo.get("stars", 0)})
        print(f"{verdict} {score}/10")

        # DELETE CLONE immediately
        shutil.rmtree(repo_path, ignore_errors=True)

        time.sleep(1)

    print(f"✅ RE complete: {len(results)} repos analyzed")
    return results


# ── Update Knowledge Base ───────────────────────────────────────
def update_knowledge_base(scraped_repos):
    """Write discovered repos to the appropriate category files."""
    print("📝 Updating knowledge base...")

    # Group by category based on topics/description
    categories = {}
    for repo in scraped_repos:
        name = repo["full_name"].lower()
        desc = (repo.get("description") or "").lower()
        topics = [t.lower() for t in repo.get("topics", [])]

        cat = "other"
        if any(k in name + desc + " ".join(topics) for k in ["llm", "language model", "gpt", "llama", "qwen", "deepseek", "glm", "baichuan", "yi-", "kimi", "mistral"]):
            cat = "01-ai-models"
        elif any(k in name + desc + " ".join(topics) for k in ["image", "diffusion", "stable diffusion", "flux", "dall-e", "midjourney", "kolors", "cogview"]):
            cat = "04-image-generation"
        elif any(k in name + desc + " ".join(topics) for k in ["video", "sora", "wan", "cogvideo", "hunyuan video", "kling", "pika", "runway"]):
            cat = "05-video-generation"
        elif any(k in name + desc + " ".join(topics) for k in ["speech", "tts", "audio", "whisper", "bark", "music", "cosyvoice", "f5-tts", "chattts", "vocos"]):
            cat = "06-audio-music"
        elif any(k in name + desc + " ".join(topics) for k in ["agent", "autogpt", "crewai", "autogen", "deer-flow", "agentic"]):
            cat = "08-ai-agents"
        elif any(k in name + desc + " ".join(topics) for k in ["rag", "retrieval", "vector", "embedding", "knowledge", "graphrag", "lightrag"]):
            cat = "09-rag-knowledge"
        elif any(k in name + desc + " ".join(topics) for k in ["coding", "copilot", "codeium", "codex", "code assistant", "tabnine", "cody"]):
            cat = "03-coding-tools"
        elif any(k in name + desc + " ".join(topics) for k in ["local", "ollama", "llama.cpp", "vllm", "tgi", "lmstudio", "gpt4all", "jan"]):
            cat = "10-local-llms"
        elif any(k in name + desc + " ".join(topics) for k in ["chinese", "中文", "china", "alibaba", "tencent", "baidu", "bytedance", "deepseek", "qwen", "glm", "baichuan"]):
            cat = "21-chinese-ai-ecosystem"
        elif any(k in name + desc + " ".join(topics) for k in ["esp32", "esp-", "embedded", "microcontroller", "edge", "tinyml", "micro"]):
            cat = "24-esp-embedded-ai"

        categories.setdefault(cat, []).append(repo)

    # Write to category files
    written = 0
    for cat, repos in categories.items():
        cat_dir = REPO_ROOT / cat
        if not cat_dir.exists():
            continue
        # Find the main md file
        md_files = list(cat_dir.glob("*.md"))
        if not md_files:
            continue
        target = md_files[0]

        existing = target.read_text()
        existing_names = set(re.findall(r'\[([^\]]+)\]\(https://github\.com/[^)]+\)', existing))

        new_repos = [r for r in repos if r["full_name"] not in existing_names]
        if not new_repos:
            continue

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        section = f"\n\n## 🆕 Auto-discovered {NODE} ({ts})\n\n"
        section += "| Repo | Stars | Lang | Description |\n"
        section += "|------|-------|------|-------------|\n"
        for r in sorted(new_repos, key=lambda x: x.get("stars", 0), reverse=True)[:50]:
            name = r["full_name"]
            url = r.get("url", f"https://github.com/{name}")
            stars = r.get("stars", 0)
            lang = r.get("language", "?")
            desc = (r.get("description") or "")[:70]
            section += f"| [{name}]({url}) | ⭐{stars} | {lang} | {desc} |\n"

        with open(target, "a") as f:
            f.write(section)
        written += len(new_repos)
        print(f"  {cat}: +{len(new_repos)} repos")

    print(f"✅ Knowledge base updated: {written} new repos written")


# ── Git Push ────────────────────────────────────────────────────
def git_push():
    """Commit and push everything."""
    print("📤 Pushing to git...")
    try:
        os.chdir(REPO_ROOT)
        subprocess.run(["git", "config", "user.name", f"Library Bot ({NODE})"], check=True)
        subprocess.run(["git", "config", "user.email", "bot@library-of-alexander"], check=True)
        subprocess.run(["git", "add", "-A"], check=True)

        # Check if there are changes
        r = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True)
        if not r.stdout.strip():
            print("  No changes to push")
            return

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        msg = f"🔄 [{NODE}] Auto-update {ts} — {r.stdout.strip().count(chr(10))} files changed"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, timeout=60)
        print(f"✅ Pushed: {msg}")
    except Exception as e:
        print(f"❌ Push failed: {e}")


# ── Main Loop ───────────────────────────────────────────────────
def run_once():
    """One full cycle: scrape → RE → update → push."""
    start = time.time()
    print(f"\n{'='*60}")
    print(f"🏛️ Library of Alexander — {NODE}")
    print(f"Time: {datetime.now(timezone.utc).isoformat()} UTC")
    print(f"Scratch: {scratch_usage_gb():.1f}GB / {S['max_gb']}GB")
    print(f"{'='*60}")

    # 1. Scrape
    scraped = scrape_all()

    # 2. Reverse engineer our target repos
    re_targets = [{"full_name": n} for n in get_re_targets()]
    re_results = reverse_engineer(re_targets)

    # 3. Also RE any newly discovered high-star repos
    new_high_star = [r for r in scraped if r.get("stars", 0) > 1000 and r["full_name"] not in {t["full_name"] for t in re_targets}]
    if new_high_star:
        print(f"\n🔬 RE {len(new_high_star)} newly discovered high-star repos...")
        re_results.extend(reverse_engineer(new_high_star[:20]))  # Cap at 20

    # 4. Update knowledge base
    update_knowledge_base(scraped)

    # 5. Push
    git_push()

    # 6. Save summary
    summary = {
        "node": NODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scraped": len(scraped),
        "re_analyzed": len(re_results),
        "duration_seconds": round(time.time() - start, 1),
    }
    (DATA / f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.json").write_text(json.dumps(summary, indent=2))

    print(f"\n✅ Cycle complete in {summary['duration_seconds']}s")
    print(f"   Scraped: {summary['scraped']} | RE: {summary['re_analyzed']}")
    print(f"   Scratch: {scratch_usage_gb():.1f}GB")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        run_once()
    else:
        # Continuous loop: run every 4 hours, clean scratch every 5 hours
        last_run = 0
        last_clean = time.time()
        RUN_INTERVAL = 4 * 3600      # 4 hours
        CLEAN_INTERVAL = 5 * 3600    # 5 hours

        print(f"🏛️ Library of Alexander — {NODE} (continuous mode)")
        print(f"Run interval: {RUN_INTERVAL/3600}h | Clean interval: {CLEAN_INTERVAL/3600}h")

        while True:
            now = time.time()

            # Clean scratch every 5 hours
            if now - last_clean >= CLEAN_INTERVAL:
                cleanup_scratch()
                last_clean = now

            # Run pipeline every 4 hours
            if now - last_run >= RUN_INTERVAL:
                try:
                    run_once()
                except Exception as e:
                    print(f"❌ Pipeline error: {e}")
                last_run = now

            # Sleep for 5 minutes between checks
            time.sleep(300)
