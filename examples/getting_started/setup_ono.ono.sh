#!/bin/bash
# ?ono
# type=config
# model=Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF
# ?

# Check for LLM backends
<?ono detect which LLM backends are available (ollama, sglang, llama.cpp, vllm) and return the first one found ?>

# Get available models if ollama
<?ono if ollama is available, list available models and return the first one. if no models exist, return "no_models" ?>

<?ono if model is "no_models", download Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF model using ollama pull ?>

# Start TCP server
<?ono start a TCP server on port 8080 that processes ono blocks and returns results ?>
