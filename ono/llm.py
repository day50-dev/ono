"""LLM client for Ollama API."""

import httpx
import asyncio


class LLMClient:
    def __init__(self, api_url: str, model: str, api_key: str = None):
        self.api_url = api_url
        self.model = model
        self.api_key = api_key

    async def generate_async(self, prompt: str, history: list = None, options: dict = None):
        """Generate text using the Ollama API."""
        url = f"{self.api_url}/chat/completions"
        
        messages = []
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
        }
        if options:
            payload.update(options)
        
        timeout = httpx.Timeout(timeout=120.0, connect=10.0, read=120.0, write=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def generate(self, prompt: str, history: list = None, options: dict = None):
        """Synchronous wrapper for generate_async."""
        return asyncio.run(self.generate_async(prompt, history, options))
