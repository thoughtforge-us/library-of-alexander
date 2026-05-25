#!/usr/bin/env python3
"""
Library of Alexander — Distributed Scraping Configuration
Runs across the NexusAI swarm with per-node rate limits and storage management.
"""

import os
import socket
from pathlib import Path

# ── Node Detection ──────────────────────────────────────────────
HOSTNAME = socket.gethostname()
TAILSCALE_IP = os.environ.get("TAILSCALE_IP", "")

# Determine which node we're on
if HOSTNAME == "nexus" or "nexus" in HOSTNAME:
    NODE = "nexus"
elif HOSTNAME == "jupiter" or "jupiter" in HOSTNAME:
    NODE = "jupiter"
elif HOSTNAME == "luna" or "luna" in HOSTNAME or TAILSCALE_IP == "100.89.31.123":
    NODE = "luna"
else:
    NODE = "unknown"

# ── Storage Paths ───────────────────────────────────────────────
# Each node uses its local spare SSD for scratch, cleans up after itself

STORAGE = {
    "nexus": {
        "scratch": Path("/tmp/luna-ssd/scratch"),      # 444GB spare SSD
        "clones": Path("/tmp/luna-ssd/scratch/clones"),
        "analysis": Path("/tmp/luna-ssd/scratch/analysis"),
        "reports": Path("/tmp/luna-ssd/scratch/reports"),
        "data": Path("/home/donn/repos/library-of-alexander/data"),
        "max_scratch_gb": 200,        # Don't fill more than 200GB of the 444GB
        "clone_retention_hours": 2,   # Delete clones after 2 hours
        "analysis_retention_days": 7, # Keep analysis for 7 days
    },
    "jupiter": {
        "scratch": Path("/mnt/ssd-data/scratch"),      # Jupiter's SSD
        "clones": Path("/mnt/ssd-data/scratch/clones"),
        "analysis": Path("/mnt/ssd-data/scratch/analysis"),
        "reports": Path("/mnt/ssd-data/scratch/reports"),
        "data": Path("/home/donn/repos/library-of-alexander/data"),
        "max_scratch_gb": 20,         # Light usage — only 20GB max
        "clone_retention_hours": 1,   # Delete clones after 1 hour
        "analysis_retention_days": 3, # Keep analysis for 3 days
    },
    "luna": {
        "scratch": Path("/mnt/scratch"),               # Pi 4 — minimal
        "clones": Path("/mnt/scratch/clones"),
        "analysis": Path("/mnt/scratch/analysis"),
        "reports": Path("/mnt/scratch/reports"),
        "data": Path("/home/donn/repos/library-of-alexander/data"),
        "max_scratch_gb": 2,          # Tiny — Pi 4 has limited space
        "clone_retention_hours": 0.5, # Delete after 30 minutes
        "analysis_retention_days": 1, # Keep analysis for 1 day
    },
}

# ── Rate Limits (per node) ──────────────────────────────────────
# Jupiter runs at lower rate to not fill its disk
RATE_LIMITS = {
    "nexus": {
        "scrape_interval_minutes": 240,    # Every 4 hours
        "repos_per_scrape": 50,            # Full scan
        "clone_timeout_seconds": 120,
        "max_concurrent_clones": 3,
        "github_api_pause_seconds": 1,     # Normal rate
    },
    "jupiter": {
        "scrape_interval_minutes": 720,    # Every 12 hours (lower rate)
        "repos_per_scrape": 15,            # Light scan
        "clone_timeout_seconds": 60,
        "max_concurrent_clones": 1,
        "github_api_pause_seconds": 3,     # Slower to avoid rate limits
    },
    "luna": {
        "scrape_interval_minutes": 1440,   # Once per day (minimal)
        "repos_per_scrape": 5,             # Very light
        "clone_timeout_seconds": 30,
        "max_concurrent_clones": 1,
        "github_api_pause_seconds": 5,     # Slowest
    },
}

# ── Current Node Config ─────────────────────────────────────────
NODE_STORAGE = STORAGE.get(NODE, STORAGE["nexus"])
NODE_RATE = RATE_LIMITS.get(NODE, RATE_LIMITS["nexus"])

# ── GitHub Targets ──────────────────────────────────────────────
CHINESE_ORGS = [
    "deepseek-ai", "QwenLM", "THUDM", "InternLM", "01-ai",
    "MoonshotAI", "MiniMax-AI", "FunAudioLLM", "OpenBMB",
    "FlagOpen", "PaddlePaddle", "baichuan-inc", "modelscope",
    "TencentARC", "Kwai-Kolors", "Wan-Video", "OpenGVLab",
    "IDEA-CCNL", "netease-youdao", "stepfun-ai",
]

MAJOR_ORGS = [
    "openai", "meta-llama", "microsoft", "huggingface",
    "stability-ai", "vllm-project", "langchain-ai", "run-llama",
    "crewAIInc", "ggerganov", "comfyanonymous", "lllyasviel",
]

# Repos to reverse engineer (full list for nexus, subset for jupiter)
RE_FULL_REPOS = [
    "langchain-ai/langchain", "run-llama/llama_index",
    "crewAIInc/crewAI", "microsoft/autogen",
    "google/adk-python", "letta-ai/letta",
    "deepset-ai/haystack", "agno-agi/agno",
    "mastra-ai/mastra", "bytedance/deer-flow",
    "ggerganov/llama.cpp", "comfyanonymous/ComfyUI",
    "lllyasviel/ControlNet", "openai/whisper",
    "suno-ai/bark", "huggingface/diffusers",
    "Stability-AI/generative-models", "CompVis/stable-diffusion",
    "vllm-project/vllm", "openai/codex",
    "anthropics/claude-cookbooks", "infiniflow/ragflow",
    "HKUDS/LightRAG", "microsoft/graphrag",
    "mem0ai/mem0", "thedotmack/claude-mem",
    "lobehub/lobehub", "langflow-ai/langflow",
    "langgenius/dify", "FlowiseAI/Flowise",
    "Shubhamsaboo/awesome-llm-apps", "NousResearch/hermes-agent",
    "msitarzewski/agency-agents", "browser-use/browser-use",
    "karpathy/autoresearch", "OpenHands/OpenHands",
    "hiyouga/LLaMA-Factory", "FoundationAgents/MetaGPT",
    "deepseek-ai/DeepSeek-V3", "QwenLM/Qwen3",
    "Wan-Video/Wan2.1", "FunAudioLLM/CosyVoice",
    "FunAudioLLM/F5-TTS", "2noise/ChatTTS",
    "Kwai-Kolors/Kolors", "TencentARC/GFPGAN",
    "FlagOpen/FlagEmbedding", "OpenBMB/MiniCPM",
    "modelscope/ms-swift", "modelscope/FunASR",
]

# Jupiter only does a lightweight subset
RE_JUPITER_REPOS = [
    "langchain-ai/langchain", "ggerganov/llama.cpp",
    "vllm-project/vllm", "openai/whisper",
    "infiniflow/ragflow", "mem0ai/mem0",
    "deepseek-ai/DeepSeek-V3", "QwenLM/Qwen3",
    "Wan-Video/Wan2.1", "FunAudioLLM/CosyVoice",
    "2noise/ChatTTS", "Kwai-Kolors/Kolors",
    "FlagOpen/FlagEmbedding", "OpenBMB/MiniCPM",
]

def get_re_targets():
    """Return the right set of RE targets for this node."""
    if NODE == "jupiter":
        return RE_JUPITER_REPOS
    return RE_FULL_REPOS


# ── Cleanup ─────────────────────────────────────────────────────
def get_scratch_usage_gb(path: Path) -> float:
    """Get total size of scratch directory in GB."""
    total = 0
    try:
        for f in path.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
    except Exception:
        pass
    return total / (1024 ** 3)


def cleanup_scratch(storage_config: dict):
    """Clean up scratch space if over limit."""
    scratch = storage_config["scratch"]
    max_gb = storage_config["max_scratch_gb"]
    usage = get_scratch_usage_gb(scratch)

    if usage <= max_gb:
        return

    print(f"⚠️ Scratch usage {usage:.1f}GB > {max_gb}GB limit. Cleaning up...")

    # Delete oldest clone directories first
    clones_dir = storage_config["clones"]
    if clones_dir.exists():
        dirs = sorted(clones_dir.iterdir(), key=lambda d: d.stat().st_mtime)
        for d in dirs[:len(dirs) // 2]:  # Delete oldest half
            import shutil
            shutil.rmtree(d, ignore_errors=True)
            print(f"  🗑️ Deleted {d.name}")

    # Delete old analysis files
    analysis_dir = storage_config["analysis"]
    if analysis_dir.exists():
        import time
        retention_secs = storage_config["analysis_retention_days"] * 86400
        cutoff = time.time() - retention_secs
        for f in analysis_dir.rglob("*"):
            if f.is_file() and f.stat().st_mtime < cutoff:
                f.unlink(missing_ok=True)

    print(f"✅ Cleanup done. New usage: {get_scratch_usage_gb(scratch):.1f}GB")
