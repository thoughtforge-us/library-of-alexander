#!/usr/bin/env python3
"""
Library of Alexander — Distributed Configuration
Every node scrapes GitHub, reverse engineers repos, pushes to git every 4h.
Scratch deleted every 5h to ensure nothing missed accumulates.
"""

import os, socket, shutil, time, json
from pathlib import Path
from datetime import datetime, timezone

# ── Node Detection ──────────────────────────────────────────────
HOSTNAME = socket.gethostname()
TAILSCALE_IP = os.environ.get("TAILSCALE_IP", "")

if HOSTNAME in ("nexus",) or "nexus" in HOSTNAME:
    NODE = "nexus"
elif HOSTNAME in ("jupiter",) or "jupiter" in HOSTNAME:
    NODE = "jupiter"
elif HOSTNAME in ("luna",) or "luna" in HOSTNAME or TAILSCALE_IP == "100.89.31.123":
    NODE = "luna"
else:
    NODE = "unknown"

# ── Storage (local SSD on each node) ────────────────────────────
STORAGE = {
    "nexus": {
        "scratch":    Path("/mnt/storage/scratch"),
        "clones":     Path("/mnt/storage/scratch/clones"),
        "analysis":   Path("/mnt/storage/scratch/analysis"),
        "reports":    Path("/mnt/storage/scratch/reports"),
        "data":       Path("/home/donn/repos/library-of-alexander/data"),
        "max_gb":     20,
    },
    "jupiter": {
        "scratch":    Path("/mnt/ssd-data/scratch"),
        "clones":     Path("/mnt/ssd-data/scratch/clones"),
        "analysis":   Path("/mnt/ssd-data/scratch/analysis"),
        "reports":    Path("/mnt/ssd-data/scratch/reports"),
        "data":       Path("/home/donn/library-of-alexander/data"),
        "max_gb":     10,
    },
    "luna": {
        "scratch":    Path("/mnt/scratch"),
        "clones":     Path("/mnt/scratch/clones"),
        "analysis":   Path("/mnt/scratch/analysis"),
        "reports":    Path("/mnt/scratch/reports"),
        "data":       Path("/home/donn/library-of-alexander/data"),
        "max_gb":     10,
    },
}

S = STORAGE.get(NODE, STORAGE["nexus"])
for d in ["scratch", "clones", "analysis", "reports", "data"]:
    S[d].mkdir(parents=True, exist_ok=True)

# ── Scrape Targets ──────────────────────────────────────────────
# Everything we care about — broad queries to catch everything
GITHUB_QUERIES = {
    "llm":              "LLM language model stars:>50",
    "chinese_ai":       "chinese AI 中文 stars:>20",
    "image_gen":        "image generation diffusion stars:>50",
    "video_gen":        "video generation stars:>50",
    "audio_tts":        "text to speech TTS stars:>50",
    "music_gen":        "music generation stars:>50",
    "ai_agent":         "AI agent autonomous stars:>50",
    "rag":              "RAG retrieval augmented stars:>50",
    "coding_ai":        "AI coding assistant copilot stars:>50",
    "local_llm":        "local LLM inference stars:>50",
    "fine_tuning":      "fine-tuning LLM stars:>50",
    "embedding":        "embedding model stars:>50",
    "multimodal":       "multimodal vision language stars:>50",
    "robotics_ai":      "robotics AI stars:>20",
    "edge_ai":          "edge AI embedded stars:>20",
    "mcp":              "MCP model context protocol stars:>20",
    "esp32_ai":         "ESP32 AI stars:>10",
    "embedded_ai":      "embedded AI microcontroller stars:>10",
    "distributed_ai":   "distributed AI inference stars:>20",
    "ai_infrastructure": "AI infrastructure serving stars:>20",
    "prompt_engineering": "prompt engineering stars:>20",
    "ai_security":      "AI security safety stars:>20",
    "ai_hardware":      "AI hardware GPU stars:>20",
    "open_source_ai":   "open source AI stars:>100",
    "ai_tools":         "AI tools productivity stars:>50",
    "ai_automation":    "AI automation workflow stars:>50",
    "computer_vision":  "computer vision stars:>50",
    "nlp":              "NLP natural language stars:>50",
    "speech_recognition": "speech recognition ASR stars:>20",
    "voice_cloning":    "voice cloning stars:>20",
    "image_editing":    "image editing AI stars:>50",
    "upscale":          "upscale super resolution stars:>20",
    "3d_generation":    "3D generation stars:>20",
    "ai_search":        "AI search engine stars:>20",
    "ai_database":      "vector database stars:>20",
    "ai_monitoring":    "AI monitoring observability stars:>10",
    "ai_deployment":    "AI deployment serving stars:>20",
    "ai_evaluation":    "AI evaluation benchmark stars:>20",
    "ai_framework":     "AI framework stars:>50",
    "ai_platform":      "AI platform stars:>50",
    "ai_startup":       "AI startup stars:>10",
    "ai_education":     "AI education tutorial stars:>20",
    "ai_book":          "AI book course stars:>20",
    "ai_dataset":       "AI dataset stars:>20",
    "ai_model_hub":     "model hub stars:>20",
    "ai_api":           "AI API stars:>20",
    "ai_cli":           "AI CLI tool stars:>20",
    "ai_gui":           "AI GUI interface stars:>20",
    "ai_notebook":      "AI Jupyter notebook stars:>20",
    "ai_docker":        "AI docker container stars:>10",
    "ai_kubernetes":    "AI kubernetes stars:>10",
}

# Chinese AI orgs — comprehensive
CHINESE_ORGS = [
    "deepseek-ai", "QwenLM", "THUDM", "InternLM", "01-ai",
    "MoonshotAI", "MiniMax-AI", "FunAudioLLM", "OpenBMB",
    "FlagOpen", "PaddlePaddle", "baichuan-inc", "modelscope",
    "TencentARC", "Kwai-Kolors", "Wan-Video", "OpenGVLab",
    "IDEA-CCNL", "netease-youdao", "stepfun-ai", "ZhipuAI",
    "Tencent", "bytedance", "alibaba", "baidu",
]

# Major Western AI orgs
WESTERN_ORGS = [
    "openai", "meta-llama", "microsoft", "huggingface",
    "stability-ai", "vllm-project", "langchain-ai", "run-llama",
    "crewAIInc", "ggerganov", "comfyanonymous", "lllyasviel",
    "google-deepmind", "anthropic", "mistralai", "xai",
    "nvidia", "intel", "apple", "facebook",
]

# Individual repos to RE — our specific interests
RE_TARGETS = {
    "nexus": [  # Full list — nexus does the heavy lifting
        # Agent frameworks
        "langchain-ai/langchain", "run-llama/llama_index",
        "crewAIInc/crewAI", "microsoft/autogen",
        "google/adk-python", "letta-ai/letta",
        "agno-agi/agno", "mastra-ai/mastra",
        "bytedance/deer-flow", "FoundationAgents/MetaGPT",
        "NousResearch/hermes-agent", "msitarzewski/agency-agents",
        "Significant-Gravitas/AutoGPT", "OpenHands/OpenHands",
        "mem0ai/mem0", "thedotmack/claude-mem",
        "hiyouga/LLaMA-Factory", "modelscope/ms-swift",
        # Image/Video
        "huggingface/diffusers", "comfyanonymous/ComfyUI",
        "lllyasviel/ControlNet", "lllyasviel/Fooocus",
        "Stability-AI/generative-models", "CompVis/stable-diffusion",
        "AUTOMATIC1111/stable-diffusion-webui",
        "Wan-Video/Wan2.1", "Wan-Video/Wan2.2",
        "THUDM/CogVideoX", "TencentARC/GFPGAN",
        "TencentARC/PhotoMaker", "TencentARC/InstantMesh",
        "Kwai-Kolors/Kolors", "Tencent-Hunyuan/HunyuanImage-2.1",
        # Audio
        "openai/whisper", "suno-ai/bark",
        "FunAudioLLM/CosyVoice", "FunAudioLLM/F5-TTS",
        "2noise/ChatTTS", "FunAudioLLM/SenseVoice",
        "modelscope/FunASR", "netease-youdao/EmotiVoice",
        # Local LLMs / Serving
        "ggerganov/llama.cpp", "vllm-project/vllm",
        "oobabooga/text-generation-webui",
        "Mozilla-Ocho/llamafile", "ml-explore/mlx",
        # RAG / Knowledge
        "infiniflow/ragflow", "HKUDS/LightRAG",
        "microsoft/graphrag", "weaviate/Verba",
        "SciPhi-AI/R2R", "truefoundry/cognita",
        "FlagOpen/FlagEmbedding",
        # Coding AI
        "openai/codex", "anthropics/claude-cookbooks",
        "Codium-ai/pr-agent", "continuedev/continue",
        "sourcegraph/cody", "TabNine/tabnine-vscode",
        # Platforms
        "langflow-ai/langflow", "langgenius/dify",
        "FlowiseAI/Flowise", "lobehub/lobehub",
        "Shubhamsaboo/awesome-llm-apps",
        "browser-use/browser-use", "firecrawl/firecrawl",
        # Chinese LLMs
        "deepseek-ai/DeepSeek-V3", "deepseek-ai/DeepSeek-R1",
        "QwenLM/Qwen3", "THUDM/ChatGLM3",
        "OpenBMB/MiniCPM", "01-ai/Yi",
        "MoonshotAI/Kimi-K2.5", "MiniMax-AI/MiniMax-M1",
        "baichuan-inc/Baichuan2", "InternLM/InternLM",
        # ESP32 / Embedded AI
        "espressif/esp-dl", "espressif/esp-dsp",
        "espressif/esp-claw",
        # Infrastructure
        "open-webui/open-webui", "Mintplex-Labs/anything-llm",
        "karpathy/autoresearch",
    ],
    "jupiter": [  # Subset — lighter load
        "langchain-ai/langchain", "ggerganov/llama.cpp",
        "vllm-project/vllm", "openai/whisper",
        "infiniflow/ragflow", "mem0ai/mem0",
        "deepseek-ai/DeepSeek-V3", "QwenLM/Qwen3",
        "Wan-Video/Wan2.1", "FunAudioLLM/CosyVoice",
        "2noise/ChatTTS", "Kwai-Kolors/Kolors",
        "FlagOpen/FlagEmbedding", "OpenBMB/MiniCPM",
        "openai/codex", "huggingface/diffusers",
        "comfyanonymous/ComfyUI", "lllyasviel/ControlNet",
    ],
    "luna": [  # Minimal — Pi 4
        "ggerganov/llama.cpp", "openai/whisper",
        "deepseek-ai/DeepSeek-V3", "QwenLM/Qwen3",
        "2noise/ChatTTS", "espressif/esp-dl",
    ],
}


def get_re_targets():
    return RE_TARGETS.get(NODE, RE_TARGETS["nexus"])


def scratch_usage_gb():
    total = 0
    try:
        for f in S["scratch"].rglob("*"):
            if f.is_file():
                total += f.stat().st_size
    except:
        pass
    return total / (1024**3)


def cleanup_scratch():
    """Delete everything in scratch."""
    usage = scratch_usage_gb()
    print(f"🧹 Cleaning scratch: {usage:.1f}GB")
    try:
        for item in S["scratch"].iterdir():
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)
        # Recreate dirs
        for d in ["clones", "analysis", "reports"]:
            S[d].mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"  Cleanup error: {e}")
    print(f"✅ Scratch clean: {scratch_usage_gb():.1f}GB")
