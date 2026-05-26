# LiteLLM — Reverse Engineering Analysis

**Repo**: github.com/BerriAI/litellm  
**Stars**: 20,000+  
**Language**: Python  
**Category**: LLM Proxy/Router

## Architecture

LiteLLM is a LLM proxy and router that provides a unified OpenAI-compatible API for 100+ LLM providers.

## Key Design Patterns

1. **Unified API** — Single API for all LLM providers
2. **Load balancing** — Distribute requests across providers
3. **Fallback chain** — Automatic fallback if provider fails
4. **Cost tracking** — Track spending across providers
5. **Caching** — Cache responses to reduce costs

## What We Can Learn

- Unified API simplifies provider switching
- Load balancing improves reliability and performance
- Fallback chain prevents single points of failure
- Cost tracking enables budget management
- Caching reduces costs and latency

## Integration Ideas

- Deploy LiteLLM on Luna as fleet LLM proxy
- Use load balancing across local + cloud providers
- Implement fallback chain for reliability
- Add cost tracking for budget management
- Enable caching for common queries
