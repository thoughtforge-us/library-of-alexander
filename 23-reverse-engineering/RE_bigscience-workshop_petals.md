# Petals — Reverse Engineering Analysis

**Repo**: github.com/bigscience-workshop/petals  
**Stars**: 25,000+  
**Language**: Python  
**Category**: Distributed LLM Inference

## Architecture

Petals enables running large LLMs collaboratively across multiple machines, with each machine hosting a portion of the model.

## Key Design Patterns

1. **Collaborative inference** — Multiple machines run different model layers
2. **DHT-based discovery** — Distributed hash table for peer discovery
3. **Block hosting** — Each peer hosts specific model blocks
4. **Adaptive routing** — Requests routed to peers with needed blocks
5. **Fault tolerance** — System continues if peers disconnect

## What We Can Learn

- Collaborative inference enables running very large models
- DHT-based discovery is scalable for large networks
- Block hosting allows specialization per device
- Adaptive routing optimizes request handling
- Fault tolerance is essential for distributed systems

## Integration Ideas

- Deploy Petals across our fleet for large model inference
- Use DHT for peer discovery and coordination
- Assign model blocks based on device capabilities
- Implement adaptive routing for optimal performance
- Add fault tolerance for reliable operation
