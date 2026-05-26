# FastChat — Reverse Engineering Analysis

**Repo**: github.com/lm-sys/FastChat  
**Stars**: 35,000+  
**Language**: Python  
**Category**: Model Serving

## Architecture

FastChat is an open platform for training, serving, and evaluating large language models, powering Vicuna and Chatbot Arena.

## Key Design Patterns

1. **Multi-model serving** — Serve multiple models from single instance
2. **Load balancing** — Distribute requests across model instances
3. **API compatibility** — OpenAI-compatible API
4. **Evaluation framework** — Built-in model evaluation
5. **Web UI** — Chat interface for model interaction

## What We Can Learn

- Multi-model serving enables A/B testing and fallback
- Load balancing improves throughput and reliability
- OpenAI-compatible API enables drop-in replacement
- Evaluation framework enables continuous improvement
- Web UI provides easy access for users

## Integration Ideas

- Deploy FastChat on Nexus for multi-model serving
- Use load balancing for high-throughput scenarios
- Implement OpenAI-compatible API for fleet agents
- Add evaluation framework for model comparison
- Create web UI for fleet model access
