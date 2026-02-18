#!/bin/bash
# Setup and start TCP Ono server

<?ono detect available LLM backends (ollama, sglang, llama.cpp, vllm) ?>

<?ono if ollama is available, list available models ?>

<?ono if no models found, download Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF ?>

<?ono start TCP server on port 8080 ?>

echo "TCP Ono server is running!"
echo "Send queries like: echo '[?ono your query?]' | nc localhost 8080"
