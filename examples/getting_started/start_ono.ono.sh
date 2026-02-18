#!/bin/bash
# Start Ono TCP server with automatic model detection

<?ono 
detect which LLM backends are available (ollama, sglang, llama.cpp, vllm)
if ollama is available, check for models
if no models found, download Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF using ollama pull
return the detected backend and model name
?>

<?ono start a TCP server on port 8080 that processes ono blocks and returns results ?>

# Usage:
# bash start_ono.ono.sh
# Then: echo '[?ono find process on port 8080?]' | nc localhost 8080
