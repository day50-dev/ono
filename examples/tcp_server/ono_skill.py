#!/usr/bin/env python3
"""ono skill for TCP server with model detection and setup."""

import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ono.parser import OnoParser
from ono.llm import LLMClient
from ono.processor import Processor


def detect_backend():
    """Detect which LLM backend is available."""
    backends = []
    
    try:
        result = subprocess.run(['which', 'ollama'], capture_output=True)
        if result.returncode == 0:
            backends.append('ollama')
    except:
        pass
    
    try:
        result = subprocess.run(['which', 'sglang'], capture_output=True)
        if result.returncode == 0:
            backends.append('sglang')
    except:
        pass
    
    try:
        result = subprocess.run(['which', 'llama-server'], capture_output=True)
        if result.returncode == 0:
            backends.append('llama.cpp')
    except:
        pass
    
    try:
        result = subprocess.run(['which', 'vllm'], capture_output=True)
        if result.returncode == 0:
            backends.append('vllm')
    except:
        pass
    
    return backends


def get_ollama_models():
    """Get list of available Ollama models."""
    try:
        req = urllib.request.Request('http://localhost:11434/api/tags')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return [model['name'] for model in data.get('models', [])]
    except:
        return []


def download_ollama_model(model_name):
    """Download an Ollama model."""
    try:
        cmd = ['ollama', 'pull', model_name]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def process_request(request: str, llm_client: LLMClient) -> str:
    """Process an Ono request and return the result."""
    parser = OnoParser()
    parsed = parser.parse(request)
    blocks = parser.extract_ono_blocks(parsed)
    
    if not blocks:
        return request
    
    processor = Processor(llm_client)
    
    resolved_blocks = []
    for block in blocks:
        resolved = processor.process(block, format_hint='bash')
        resolved_blocks.append(resolved)
    
    result = []
    block_index = 0
    for item in parsed:
        if item.type == 'text':
            result.append(item.content)
        elif item.type == 'ono':
            if block_index < len(resolved_blocks):
                result.append(resolved_blocks[block_index])
                block_index += 1
            else:
                result.append(f'<?ono {item.content} ?>')
    
    return ''.join(result)


def main():
    """Main entry point."""
    print("=== Ono TCP Server Setup ===")
    print()
    
    backends = detect_backend()
    if not backends:
        print("No LLM backends detected.")
        print("Please install one of: ollama, sglang, llama.cpp, vllm")
        sys.exit(1)
    
    print(f"Detected backends: {', '.join(backends)}")
    
    if 'ollama' in backends:
        models = get_ollama_models()
        if models:
            print(f"Available Ollama models: {', '.join(models)}")
            default_model = models[0]
        else:
            print("No Ollama models found.")
            default_model = 'Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF'
            print(f"Will use: {default_model}")
            print("Downloading model...")
            if download_ollama_model(default_model):
                print("Download complete!")
            else:
                print("Download failed. Please check your connection.")
                sys.exit(1)
    else:
        print("Using first available backend")
        default_model = 'default'
    
    print()
    print("Starting TCP server...")
    print(f"Use: echo '[?ono your query?]' | nc localhost 8080")
    
    from ono_tcp import main as tcp_main
    tcp_main()


if __name__ == '__main__':
    main()
