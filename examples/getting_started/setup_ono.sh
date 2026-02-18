#!/bin/bash
# ?ono
# type=config
# model=Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF
# ?

# Check for LLM backends
for backend in ollama sglang llama.cpp vllm; do command -v "$backend" >/dev/null 2>&1 && echo "$backend" && break; done

# Get available models if ollama
command -v ollama >/dev/null 2>&1 && ollama list --format json 2>/dev/null | jq -r '.models[0].name // "no_models"' || echo "no_models"

[[ "$model" == "no_models" ]] && ollama pull "Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF"

# Start TCP server
nc -l -p 8080 -e 'while IFS= read -r block; do echo "Processed: $block"; done'
