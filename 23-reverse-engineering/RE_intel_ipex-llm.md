# IPEX-LLM — Reverse Engineering Analysis

**Repo**: github.com/intel/ipex-llm  
**Stars**: 8,812  
**Language**: Python  
**Category**: Local LLM Acceleration

## Architecture

IPEX-LLM accelerates local LLM inference on Intel hardware (CPU, GPU, XPU). It supports LLaMA, Mistral, Qwen, DeepSeek, and many other models.

## Key Design Patterns

1. **Hardware-aware optimization** — Different optimizations for CPU vs GPU vs XPU
2. **Quantization support** — INT4, INT8, and mixed precision
3. **Model patching** — Transparently patches HuggingFace models for acceleration
4. **Pipeline parallelism** — Splits large models across multiple devices
5. **Low-bit inference** — Runs large models on constrained hardware

## What We Can Learn

- Hardware-aware optimization is critical for local LLM performance
- Transparent model patching allows using existing model code
- Low-bit inference enables running large models on small hardware
- Pipeline parallelism can distribute models across our fleet

## Integration Ideas

- Use IPEX-LLM on Jupiter (Intel HD 630) for local LLM acceleration
- Pipeline parallelism could split models across Jupiter + Nexus
- Low-bit inference for Luna's Pi (ARM CPU optimization)
