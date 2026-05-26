# People & Orgs to Follow — GitHub AI Ecosystem

Curated list of influential AI developers, researchers, and organizations.

## Core AI Developers

| User | Name | Followers | Why Follow | Blog |
|------|------|-----------|-----------|------|
| [karpathy](https://github.com/karpathy) | Andrej Karpathy | 191K | Former Tesla AI, OpenAI, llama2.c, nanoGPT | twitter.com/karpathy |
| [rasbt](https://github.com/rasbt) | Sebastian Raschka | 38K | ML author, researcher | sebastianraschka.com |
| [ggerganov](https://github.com/ggerganov) | Georgi Gerganov | 19.7K | llama.cpp creator | ggerganov.com |
| [simonw](https://github.com/simonw) | Simon Willison | 15K | Datasette, LLM tooling | simonwillison.net |
| [lilianweng](https://github.com/lilianweng) | Lilian Weng | 11.6K | OpenAI research | lilianweng.github.io |
| [hwchase17](https://github.com/hwchase17) | Harrison Chase | 9.8K | LangChain creator | - |
| [comfyanonymous](https://github.com/comfyanonymous) | comfyanonymous | 6.8K | ComfyUI creator | - |
| [steven-tey](https://github.com/steven-tey) | Steven Tey | 6K | AI tools | steventey.com |
| [VictorTaelin](https://github.com/VictorTaelin) | Victor Taelin | 5.5K | HVM/Kind, B端计算 | - |
| [oobabooga](https://github.com/oobabooga) | oobabooga | 4.9K | text-generation-webui | localbench.substack.com |
| [jerryjliu](https://github.com/jerryjliu) | Jerry Liu | 4.2K | LlamaIndex creator | - |
| [thomwolf](https://github.com/thomwolf) | Thomas Wolf | 3.5K | HuggingFace co-founder | thomwolf.io |
| [TheBloke](https://github.com/TheBloke) | TheBloke | 2.7K | LLM model quantization | huggingface.co/TheBloke |
| [patrickvonplaten](https://github.com/patrickvonplaten) | Patrick von Platen | 2K | HuggingFace diffusers | - |
| [haotian-liu](https://github.com/haotian-liu) | Haotian Liu | 1.9K | LLaVA creator | hliu.cc |
| [WoosukKwon](https://github.com/WoosukKwon) | Woosuk Kwon | 1.3K | vLLM creator | woosuk.me |
| [mshumer](https://github.com/mshumer) | Matt Shumer | 1.4K | AI product builder | - |
| [jongwook](https://github.com/jongwook) | Jong Wook Kim | - | OpenAI Whisper | - |

## AI Organizations

| Org | Followers | Description | Blog/Feed |
|-----|-----------|-------------|-----------|
| [huggingface](https://github.com/huggingface) | - | ML platform, transformers | huggingface.co/blog/feed.xml |
| [openai](https://github.com/openai) | - | OpenAI | openai.com/news/rss.xml |
| [meta-llama](https://github.com/meta-llama) | - | Meta Llama models | ai.meta.com/blog/ |
| [anthropics](https://github.com/anthropics) | - | Anthropic Claude | - |
| [mistralai](https://github.com/mistralai) | - | Mistral AI | - |
| [deepseek-ai](https://github.com/deepseek-ai) | - | DeepSeek models | - |
| [QwenLM](https://github.com/QwenLM) | - | Qwen models (Alibaba) | - |
| [vllm-project](https://github.com/vllm-project) | - | vLLM inference | - |
| [stability-ai](https://github.com/stability-ai) | 13.6K | Stable Diffusion | stability.ai |
| [xai-org](https://github.com/xai-org) | 9.6K | xAI (Grok) | x.ai |
| [THUDM](https://github.com/THUDM) | 11.8K | Tsinghua AI (ChatGLM, CogVideo) | huggingface.co/THUDM |
| [HKUDS](https://github.com/HKUDS) | 11.2K | HKU Data Science (LightRAG) | - |
| [n8n-io](https://github.com/n8n-io) | 13.5K | n8n workflow automation | n8n.io |
| [langchain-ai](https://github.com/langchain-ai) | - | LangChain | langchain.com/blog |
| [run-llama](https://github.com/run-llama) | - | LlamaIndex | llamaindex.ai/blog |
| [crewAIInc](https://github.com/crewAIInc) | - | CrewAI | - |
| [NousResearch](https://github.com/NousResearch) | 5K | Hermes models | nousresearch.com |
| [modelscope](https://github.com/modelscope) | 6K | ModelScope | modelscope.cn |
| [MoonshotAI](https://github.com/MoonshotAI) | 5.9K | Moonshot/Kimi | moonshot.ai |
| [MiniMax-AI](https://github.com/MiniMax-AI) | 6.3K | MiniMax | minimax.io |
| [OpenBMB](https://github.com/OpenBMB) | 6.3K | OpenBMB (MiniCPM) | openbmb.cn |
| [THUDM](https://github.com/THUDM) | 11.8K | Tsinghua (ChatGLM) | - |
| [01-ai](https://github.com/01-ai) | 1.2K | Yi models | 01.ai |
| [FlagOpen](https://github.com/FlagOpen) | 959 | FlagOpen/FlagEmbedding | - |
| [langgenius](https://github.com/langgenius) | 3.4K | Dify | dify.ai |
| [FlowiseAI](https://github.com/FlowiseAI) | 2K | Flowise | flowiseai.com |
| [lobehub](https://github.com/lobehub) | 3.6K | LobeHub | lobehub.com |
| [open-webui](https://github.com/open-webui) | 4.7K | Open WebUI | openwebui.com |
| [Mintplex-Labs](https://github.com/Mintplex-Labs) | 1.5K | AnythingLLM | mintplexlabs.com |
| [toeverything](https://github.com/toeverything) | 1.5K | AFFiNE | - |

## How to Follow

```bash
# Follow individual users
for user in karpathy ggerganov rasbt simonw hwchase17 jerryjliu comfyanonymous thomwolf WoosukKwon; do
  gh api -X PUT "user/following/$user" --silent
done

# Follow organizations
for org in huggingface openai meta-llama mistralai deepseek-ai QwenLM vllm-project; do
  gh api -X PUT "user/following/$org" --silent
done
```

## Personal Blog RSS Feeds

| Person | RSS Feed |
|--------|----------|
| Simon Willison | https://simonwillison.net/atom/everything/ |
| Lilian Weng | https://lilianweng.github.io/feed.xml |
| Sebastian Raschka | https://www.sebastianraschka.com/blog/feed |
| Jay Mody | https://jaykmody.com/feed.xml |
| oobabooga | https://localbench.substack.com/feed |
