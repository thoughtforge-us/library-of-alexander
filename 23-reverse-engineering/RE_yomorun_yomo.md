# Yomo — Reverse Engineering Analysis

**Repo**: github.com/yomorun/yomo  
**Stars**: 1,903  
**Language**: Rust  
**Category**: Edge AI Agent Framework

## Architecture

Yomo is a serverless AI agent framework with geo-distributed edge AI infrastructure. It enables AI agents to run close to the data source, reducing latency.

## Key Design Patterns

1. **Edge-first architecture** — Agents run at the edge, not in the cloud
2. **Streaming inference** — Continuous data streams processed in real-time
3. **Geo-distributed** — Multiple edge nodes coordinate via a mesh
4. **Rust core** — Performance-critical parts in Rust, Python bindings for agents
5. **Serverless deployment** — Agents deployed as functions, not containers

## What We Can Learn

- Edge AI reduces latency for real-time applications
- Streaming inference is more efficient than batch for continuous data
- Rust core + Python bindings is a good performance/usability tradeoff
- Geo-distributed architecture could work for our fleet

## Integration Ideas

- Use Yomo for Luna's edge AI processing (Pi-hole analytics, local LLM routing)
- Deploy lightweight agents on ESP32 devices via Yomo
- Use streaming inference for real-time fleet health monitoring
