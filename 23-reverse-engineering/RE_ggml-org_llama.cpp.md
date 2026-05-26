# llama.cpp — Reverse Engineering Analysis

**Repo**: github.com/ggml-org/llama.cpp  
**Stars**: 113,100  
**Language**: C++  
**Category**: Local LLM Inference

## Architecture

llama.cpp is a C++ library for LLM inference with minimal setup and state-of-the-art performance. It uses GGUF format for model quantization.

## Key Design Patterns

1. **GGUF format** — Efficient model storage with quantization metadata
2. **Quantization** — 2-bit to 8-bit quantization for memory efficiency
3. **CPU optimization** — AVX, AVX2, AVX-512, ARM NEON optimizations
4. **GPU offloading** --partial GPU acceleration via Vulkan, CUDA, Metal
5. **Server mode** — HTTP server with OpenAI-compatible API

## What We Can Learn

- GGUF format is the standard for local LLM models
- Quantization enables running large models on small hardware
- CPU optimization is critical for devices without GPU
- GPU offloading provides best performance when available
- OpenAI-compatible API enables drop-in replacement

## Integration Ideas

- Deploy llama.cpp on Jupiter for local LLM inference
- Use GGUF format for all local models
- Optimize for CPU on Jupiter (Intel HD 630)
- Use GPU offloading on Nexus (RTX 3050)
- Run OpenAI-compatible server for fleet agents
