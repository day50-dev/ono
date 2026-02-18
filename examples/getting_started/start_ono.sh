#!/bin/bash
# Start Ono TCP server with automatic model detection

backend=""; model=""; for b in ollama sglang llama.cpp vllm; do command -v $b &>/dev/null && backend=$b && break; done; if [[ "$backend" == "ollama" ]]; then models=$(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}'); if [[ -z "$models" ]]; then ollama pull Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF 2>/dev/null; model="Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF"; else model=$(echo "$models" | head -n1); fi; fi; echo "backend=$backend model=$model"

while true; do nc -l -p 8080 | while read line; do echo "Processing: $line"; echo "Result for $line"; done; done

# Usage:
# bash start_ono.ono.sh
# Then: echo '[?ono find process on port 8080?]' | nc localhost 8080
