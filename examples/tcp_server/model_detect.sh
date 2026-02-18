#!/bin/bash
# Model detection for TCP Ono

echo "=== Detecting LLM Backends ==="
echo ""

BACKENDS=""
if command -v ollama &> /dev/null; then
    echo "✓ ollama found"
    BACKENDS="ollama $BACKENDS"
else
    echo "✗ ollama not found"
fi

if command -v sglang &> /dev/null; then
    echo "✓ sglang found"
    BACKENDS="sglang $BACKENDS"
else
    echo "✗ sglang not found"
fi

if command -v llama-server &> /dev/null; then
    echo "✓ llama.cpp found"
    BACKENDS="llama.cpp $BACKENDS"
else
    echo "✗ llama.cpp not found"
fi

if command -v vllm &> /dev/null; then
    echo "✓ vllm found"
    BACKENDS="vllm $BACKENDS"
else
    echo "✗ vllm not found"
fi

echo ""
echo "Detected backends: $BACKENDS"

# Check for models
if echo "$BACKENDS" | grep -q ollama; then
    echo ""
    echo "=== Checking Ollama Models ==="
    MODELS=$(curl -s http://localhost:11434/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    if [ -z "$MODELS" ]; then
        echo "No models found. Available models:"
        echo "  - Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF"
        echo ""
        echo "To download: ollama pull Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF"
    else
        echo "Available models:"
        echo "$MODELS"
    fi
fi
