#!/bin/bash
# Start TCP server for Ono

HOST="hostname -I 2>/dev/null || ip route get 1.1.1.1 | awk '{print $7}'"
PORT="netstat -tuln 2>/dev/null | awk '/:LISTEN/ {print $4}' | grep -oE '[0-9]+$'"

if command -v ollama &> /dev/null && [ -n "$(ollama list 2>/dev/null | tail -n +2 | grep -v '^$')" ]; then echo "Ollama models exist"; elif command -v ollama &> /dev/null; then ollama pull Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF; else echo "Ollama not available"; fi

nc -l -p $PORT -c 'while read line; do echo "Processed: $line"; done'

# Usage:
# echo '[?ono find process on port 8080?]' | nc localhost 8080
