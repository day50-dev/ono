#!/bin/bash
# Start TCP server for Ono

HOST="<?ono get TCP server host address ?>"
PORT="<?ono get TCP server port ?>"

<?ono if ollama available with models, use that. else if ollama available without models, download Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF first ?>

<?ono start a TCP server that listens on $HOST:$PORT and processes ono blocks ?>

# Usage:
# echo '[?ono find process on port 8080?]' | nc localhost 8080
