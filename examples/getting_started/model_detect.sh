#!/bin/bash
# Detect available LLM backends

available=(); for tool in ollama sglang llama.cpp vllm; do command -v "$tool" >/dev/null 2>&1 && available+=("$tool"); done; IFS=,; echo "${available[*]}"

command -v ollama >/dev/null 2>&1 && ollama list --format json | jq -r '.models[].name' || echo "ollama not available"

ls -1 models 2>/dev/null | grep -q . || echo "no_models"

[ -z "$(command_to_find_backends)" ] && echo "no_backends" || echo "$(command_to_find_backends)"
