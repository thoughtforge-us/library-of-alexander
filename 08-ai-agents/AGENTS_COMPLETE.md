# 🤖 AI Agents — Complete Catalog

> Every agent framework, platform, and tool.reverse-engineered and documented.

---

## 🏆 The Agent Landscape (2026)

```
Agent Frameworks:
├── Single Agent
│   ├── OpenAI Agents SDK (minimal, handoffs)
│   ├── Google ADK (tool-centric, MCP)
│   ├── Agno (model-agnostic, fast)
│   └── DSPy (prompt optimization)
├── Multi-Agent
│   ├── CrewAI (role-based)
│   ├── AutoGen (conversational)
│   ├── LangGraph (graph-based)
│   ├── Mason (workflow)
│   └── msitarzewski/agency-agents (70+ personas)
├── Research Agents
│   ├── DeerFlow (ByteDance, deep research)
│   ├── OpenHands (full-stack coding)
│   ├── SWE-agent (bug fixing)
│   └── karpathy/autoresearch (ML research)
└── Memory-Enabled
    ├── Letta/MemGPT (persistent memory)
    ├── mem0ai/mem0 (universal memory)
    ├── claude-mem (session memory)
    └── MemPalace (local memory palace)
```

---

## 🥇 Top 50 AI Agent Projects (by GitHub Stars)

| Rank | Project | Stars | Description | Language |
|------|---------|-------|-------------|----------|
| 1 | [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | 111K | 100+ AI Agent & RAG apps | Python |
| 2 | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 104K | Gemini CLI agent | TypeScript |
| 3 | [browser-use/browser-use](https://github.com/browser-use/browser-use) | 95K | Browser automation for agents | Python |
| 4 | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 83K | Autonomous ML research agent | Python |
| 5 | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 81K | RAG engine | Python |
| 6 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 78K | Persistent context for agents | TypeScript |
| 7 | [lobehub/lobehub](https://github.com/lobehub/lobehub) | 77K | Agent orchestration platform | TypeScript |
| 8 | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 75K | AI-driven development | Python |
| 9 | [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | 72K | Fine-tuning 600+ LLMs | Python |
| 10 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 69K | Long-horizon SuperAgent | Python |
| 11 | [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | 68K | Multi-agent software company | Python |
| 12 | [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) | 65K | 12 lessons on agents | Jupyter |
| 13 | [mem0ai/mem0](https://github.com/mem0ai/mem0) | 57K | Universal memory layer | Python |
| 14 | [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 54K | Agent orchestration for Claude | TypeScript |
| 15 | [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 53K | Visual AI agent builder | TypeScript |
| 16 | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 52K | Role-based multi-agent | Python |
| 17 | [run-llama/llama_index](https://github.com/run-llama/llama_index) | 50K | Document agent + OCR | Python |
| 18 | [microsoft/autogen](https://github.com/microsoft/autogen) | 58K | Agentic AI framework | Python |
| 19 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 137K | Agent engineering platform | Python |
| 20 | [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 124K | Web scraping for AI agents | TypeScript |
| 21 | [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | 149K | Visual AI builder | Python |
| 22 | [langgenius/dify](https://github.com/langgenius/dify) | 142K | Agentic workflow platform | TypeScript |
| 23 | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 166K | Nous Research agent | Python |
| 24 | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 105K | 70+ agent personas | Shell |
| 25 | [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | 138K | System prompts collection | - |
| 26 | [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | 59K | Best agent harness | TypeScript |
| 27 | [earendil-works/pi](https://github.com/earendil-works/pi) | 54K | AI agent toolkit | TypeScript |
| 28 | [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | 74K | Prompt engineering guide | MDX |
| 29 | [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) | 68K | Financial data + AI agents | Python |
| 30 | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | 55K | Claude Code best practices | HTML |

---

## 🏗️ Agent Framework Deep Dives

### 1. LangChain (137K ⭐)
**Pattern:** Chain of Responsibility + Builder
**Architecture:** Prompt → LLM → Parser → Chain → Agent → Tools → Output
**Key abstractions:** Chain, Agent, Tool, Memory, Retriever
**Strengths:** Massive ecosystem, 1000+ integrations
**Weaknesses:** Overly complex, heavy deps, breaking changes
**Verdict:** 🟡 Use for prototyping, not production

### 2. LlamaIndex (50K ⭐)
**Pattern:** Document-centric RAG
**Architecture:** Documents → Index → Query Engine → Response
**Key abstractions:** Index, Query Engine, Agent, Tool
**Strengths:** Best RAG framework, great document processing
**Weaknesses:** Can be slow, complex configuration
**Verdict:** 🟢 Best for RAG-heavy applications

### 3. CrewAI (52K ⭐)
**Pattern:** Role-Based Multi-Agent
**Architecture:** Crew → [Agent(role, goal) → Task] → Output
**Key abstractions:** Agent, Task, Crew, Process
**Strengths:** Intuitive role design, good for complex workflows
**Weaknesses:** Rigid structure, limited tool ecosystem
**Verdict:** 🟢 Good for structured multi-agent workflows

### 4. AutoGen (58K ⭐)
**Pattern:** Conversational Multi-Agent
**Architecture:** UserProxy ↔ Assistant ↔ [Experts] → Output
**Key abstractions:** ConversableAgent, GroupChat, AssistantAgent
**Strengths:** Flexible conversations, strong academic foundation
**Weaknesses:** Complex config, steep learning curve
**Verdict:** 🟡 Good for research, complex for production

### 5. Google ADK
**Pattern:** Tool-Centric Agent
**Architecture:** Agent(LLM, Tools, Instructions) → [Tool Call → Result] → Output
**Key abstractions:** Agent, Tool, Session, Runner
**Strengths:** Clean design, strong MCP support, production-ready
**Weaknesses:** Google-centric, smaller community
**Verdict:** 🟢 Best for Google ecosystem integration

### 6. DeerFlow (69K ⭐) — ByteDance
**Pattern:** Sandbox + Sub-Agent Orchestration
**Architecture:** Planner → [Sub-Agent in Sandbox] → Coordinator → Output
**Key abstractions:** Planner, Coordinator, Sub-Agent, Sandbox
**Strengths:** Sandbox isolation, sub-agent specialization
**Weaknesses:** Complex setup, ByteDance-centric
**Verdict:** 🟢 Best for deep research tasks

### 7. LangFlow (149K ⭐)
**Pattern:** Visual Flow Builder
**Architecture:** Visual graph → Python code → Agent execution
**Key abstractions:** Flow, Component, Edge
**Strengths:** Visual builder, huge component library
**Weaknesses:** Can generate messy code, vendor lock-in
**Verdict:** 🟢 Best for rapid prototyping

### 8. Dify (142K ⭐)
**Pattern:** Production Agent Platform
**Architecture:** Workflow → Agents → Tools → APIs
**Key abstractions:** App, Workflow, Agent, Dataset
**Strengths:** Production-ready, great UI, RAG built-in
**Weaknesses:** Can be expensive at scale
**Verdict:** 🟢 Best for production agent apps

### 9. Flowise (53K ⭐)
**Pattern:** Open-source LangFlow alternative
**Architecture:** Visual flow → LangChain code → Execution
**Key abstractions:** Flow, Node, Connection
**Strengths:** Open source, self-hostable
**Weaknesses:** Smaller ecosystem than LangFlow
**Verdict:** 🟢 Best open-source visual agent builder

### 10. MetaGPT (68K ⭐)
**Pattern:** AI Software Company
**Architecture:** Product Manager → Architect → Engineer → Tester → Output
**Key abstractions:** Role, Action, Message, Environment
**Strengths:** Full software development lifecycle
**Weaknesses:** Can be slow, expensive token usage
**Verdict:** 🟡 Interesting for automated development

---

## 🧠 Memory Systems

| Project | Stars | Type | Description |
|---------|-------|------|-------------|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 57K | Universal memory | Memory layer for any agent |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 78K | Session memory | Persistent context across sessions |
| [letta-ai/letta](https://github.com/letta-ai/letta) | - | Persistent agent | Agents with long-term memory |
| [MemPalace](https://github.com/MemPalace/MemPalace) | - | Local memory | Hierarchical memory palace |
| [OpenBMB/ClawXMemory](https://github.com/OpenBMB/ClawXMemory) | 33 | Plugin | Multi-level memory for OpenClaw |

---

## 🌐 Browser & Web Agents

| Project | Stars | Description |
|---------|-------|-------------|
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 95K | Browser automation for AI agents |
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 124K | Web scraping for AI agents |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 75K | Full-stack coding agent |
| [ScaleCUA](https://github.com/OpenGVLab/ScaleCUA) | 1.1K | Computer use agent |

---

## 🔧 MCP (Model Context Protocol) Servers

| Server | Description | Stars |
|--------|-------------|-------|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | Official MCP servers | - |
| [OpenBMB/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP) | Coding plan MCP | 83 |
| [baichuan-inc/baichuan-mcp-servers](https://github.com/baichuan-inc/baichuan-mcp-servers) | Baichuan MCP servers | 9 |

---

## 📊 Agent Benchmarks

| Benchmark | What It Tests | Top Model |
|-----------|--------------|-----------|
| SWE-bench Verified | Real GitHub issues | Claude Opus 4.5 (80.9%) |
| WebArena | Web navigation | - |
| OSWorld | OS manipulation | - |
| AgentBench | Agent capabilities | - |
| GAIA | General AI assistants | - |
| WildClawBench | Real-world agent tasks | - |

---

*Last updated: 2026-05-25*


## 🆕 Auto-discovered nexus (2026-05-25 10:10 UTC)

| Repo | Stars | Lang | Description |
|------|-------|------|-------------|
| [openai/codex](https://github.com/openai/codex) | ⭐85456 | Rust | Lightweight coding agent that runs in your terminal |
| [alibaba/arthas](https://github.com/alibaba/arthas) | ⭐37328 | Java | Alibaba Java Diagnostic Tool Arthas/Alibaba Java诊断利器Arthas |
| [bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | ⭐35189 | TypeScript | The Open-Source Multimodal AI Agent Stack: Connecting Cutting-Edge AI  |
| [alibaba/nacos](https://github.com/alibaba/nacos) | ⭐32964 | Java | an easy-to-use dynamic service discovery, configuration and service ma |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | ⭐27500 | Python | 🤗 smolagents: a barebones library for agents that think in code. |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | ⭐23292 | Python | The batteries-included agent harness. |
| [openai/swarm](https://github.com/openai/swarm) | ⭐21526 | Python | Educational framework exploring ergonomic, lightweight multi-agent orc |
| [alibaba/page-agent](https://github.com/alibaba/page-agent) | ⭐18076 | TypeScript | JavaScript in-page GUI agent. Control web interfaces with natural lang |
| [langchain-ai/langchainjs](https://github.com/langchain-ai/langchainjs) | ⭐17719 | TypeScript | The agent engineering platform |
| [alibaba/OpenSandbox](https://github.com/alibaba/OpenSandbox) | ⭐10805 | Python | Secure, Fast, and Extensible Sandbox runtime for AI agents. |
| [bytedance/UI-TARS](https://github.com/bytedance/UI-TARS) | ⭐10730 | Python | Pioneering Automated GUI Interaction with Native Agents |
| [huggingface/skills](https://github.com/huggingface/skills) | ⭐10570 | Python | Give your agents the power of the Hugging Face ecosystem |
| [alibaba/spring-ai-alibaba](https://github.com/alibaba/spring-ai-alibaba) | ⭐9728 | Java | Agentic AI Framework for Java Developers |
| [google-deepmind/lab](https://github.com/google-deepmind/lab) | ⭐7358 | C | A customisable 3D platform for agent-based AI research |
| [openai/openai-realtime-agents](https://github.com/openai/openai-realtime-agents) | ⭐6876 | TypeScript | This is a simple demonstration of more advanced, agentic patterns buil |
| [openai/openai-cs-agents-demo](https://github.com/openai/openai-cs-agents-demo) | ⭐6378 | Python | Demo of a customer service use case implemented with the OpenAI Agents |
| [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) | ⭐6230 | Rust | OpenShell is the safe, private runtime for autonomous AI agents. |
| [crewAIInc/crewAI-examples](https://github.com/crewAIInc/crewAI-examples) | ⭐5976 | Jupyter Notebook | A collection of examples that show how to use CrewAI framework to auto |
| [google-deepmind/open_spiel](https://github.com/google-deepmind/open_spiel) | ⭐5237 | C++ | OpenSpiel is a collection of environments and algorithms for research  |
| [modelscope/ms-agent](https://github.com/modelscope/ms-agent) | ⭐4279 | Python | MS-Agent: a lightweight framework to empower agentic execution of comp |
| [google-deepmind/acme](https://github.com/google-deepmind/acme) | ⭐3986 | Python | A library of reinforcement learning components and agents |
| [openai/openai-agents-js](https://github.com/openai/openai-agents-js) | ⭐3114 | TypeScript | A lightweight, powerful framework for multi-agent workflows and voice  |
| [openai/multiagent-particle-envs](https://github.com/openai/multiagent-particle-envs) | ⭐2764 | Python | Code for a multi-agent particle environment used in the paper "Multi-A |
| [langchain-ai/social-media-agent](https://github.com/langchain-ai/social-media-agent) | ⭐2584 | TypeScript | 📲 An agent for sourcing, curating, and scheduling social media posts w |
| [NVIDIA/NeMo-Agent-Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) | ⭐2325 | Python | The NVIDIA NeMo Agent toolkit is an open-source library for efficientl |
| [stepfun-ai/gelab-zero](https://github.com/stepfun-ai/gelab-zero) | ⭐2172 | Python | STEP-GUI: The top GUI agent solution in the galaxy.  Developed by the  |
| [stepfun-ai/Step-3.5-Flash](https://github.com/stepfun-ai/Step-3.5-Flash) | ⭐2046 | C++ | Fast, Sharp & Reliable Agentic Intelligence |
| [openai/maddpg](https://github.com/openai/maddpg) | ⭐1974 | Python | Code for the MADDPG algorithm from the paper "Multi-Agent Actor-Critic |
| [langchain-ai/open-agent-platform](https://github.com/langchain-ai/open-agent-platform) | ⭐1860 | TypeScript | An open-source, no-code agent building platform. |
| [openai/multi-agent-emergence-environments](https://github.com/openai/multi-agent-emergence-environments) | ⭐1800 | Python | Environment generation code for the paper "Emergent Tool Use From Mult |
| [langchain-ai/agents-from-scratch](https://github.com/langchain-ai/agents-from-scratch) | ⭐1780 | Jupyter Notebook | Build an email assistant with human-in-the-loop and memory |
| [openai/openai-cua-sample-app](https://github.com/openai/openai-cua-sample-app) | ⭐1725 | TypeScript | Learn how to use CUA (our Computer Using Agent) via the API on multipl |
| [openai/neural-mmo](https://github.com/openai/neural-mmo) | ⭐1651 | Python | Code for the paper "Neural MMO: A Massively Multiagent Game Environmen |
| [langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent) | ⭐1634 | Python | Reference implementations of several LangChain agents as Streamlit app |
| [langchain-ai/deep-agents-ui](https://github.com/langchain-ai/deep-agents-ui) | ⭐1620 | TypeScript | Custom UI for Deep Agents |
| [openai/mle-bench](https://github.com/openai/mle-bench) | ⭐1539 | Python | MLE-bench is a benchmark for measuring how well AI agents perform at m |
| [google-deepmind/concordia](https://github.com/google-deepmind/concordia) | ⭐1439 | Python | A library for generative social simulation |
| [crewAIInc/crewAI-tools](https://github.com/crewAIInc/crewAI-tools) | ⭐1430 | Python | Extend the capabilities of your CrewAI agents with Tools |
| [OpenBMB/AgentCPM-GUI](https://github.com/OpenBMB/AgentCPM-GUI) | ⭐1369 | Python | AgentCPM-GUI: An on-device GUI agent for operating Android apps, enhan |
| [langchain-ai/deepagentsjs](https://github.com/langchain-ai/deepagentsjs) | ⭐1256 | TypeScript | The batteries included agent harness. |
| [MiniMax-AI/OpenRoom](https://github.com/MiniMax-AI/OpenRoom) | ⭐1192 | TypeScript | A browser-based desktop where AI Agent operates every app through natu |
| [OpenGVLab/ScaleCUA](https://github.com/OpenGVLab/ScaleCUA) | ⭐1114 | Python | [ICLR 2026 Oral] ScaleCUA is the open-sourced computer use agents that |
| [openai/universe-starter-agent](https://github.com/openai/universe-starter-agent) | ⭐1102 | Python | A starter agent that can solve a number of universe environments. |
| [google-deepmind/scalable_agent](https://github.com/google-deepmind/scalable_agent) | ⭐1026 | Python | A TensorFlow implementation of Scalable Distributed Deep-RL with Impor |
| [langchain-ai/agent-inbox](https://github.com/langchain-ai/agent-inbox) | ⭐994 | TypeScript | 📥 An inbox UX for interacting with human-in-the-loop agents. |
| [huggingface/meshgen](https://github.com/huggingface/meshgen) | ⭐878 | Python | Use AI Agents directly in Blender. |
| [alibaba/loongsuite-go-agent](https://github.com/alibaba/loongsuite-go-agent) | ⭐857 | Go | OpenTelemetry Compile-Time Instrumentation for Golang |
| [openai/openai-chatkit-starter-app](https://github.com/openai/openai-chatkit-starter-app) | ⭐851 | Python | Starter app to build with OpenAI ChatKit + Agent Builder |
| [openai/multiagent-competition](https://github.com/openai/multiagent-competition) | ⭐836 | Python |  Code for the paper "Emergent Complexity via Multi-agent Competition" |
| [google-deepmind/meltingpot](https://github.com/google-deepmind/meltingpot) | ⭐836 | Python | A suite of test scenarios for multi-agent reinforcement learning. |
