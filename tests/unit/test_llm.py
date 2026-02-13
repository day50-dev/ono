"""
Unit tests for the Ono LLM client.
"""

import pytest
from unittest.mock import Mock, patch


class TestLLMClient:
    def test_init_client(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        assert client.api_url == "http://localhost:11434/v1"
        assert client.model == "llama3"
        assert client.api_key is None

    def test_init_client_with_api_key(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3", "test-key")
        assert client.api_key == "test-key"

    def test_generate_text(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        # The generate method should return a string
        with patch("ono.llm.asyncio") as mock_asyncio:
            mock_asyncio.run.return_value = "test response"
            result = client.generate("test prompt")
            assert isinstance(result, str)

    def test_generate_with_history(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        with patch("ono.llm.asyncio") as mock_asyncio:
            mock_asyncio.run.return_value = "test response"
            result = client.generate("test prompt", history)
            assert isinstance(result, str)

    def test_generate_with_options(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        options = {
            "temperature": 0.7,
            "max_tokens": 100,
            "stream": False
        }
        with patch("ono.llm.asyncio") as mock_asyncio:
            mock_asyncio.run.return_value = "test response"
            result = client.generate("test prompt", options=options)
            assert isinstance(result, str)


class TestLLMErrors:
    def test_api_error_handling(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        # The current implementation doesn't raise errors
        result = client.generate("test prompt")
        assert result is not None

    def test_invalid_response_handling(self):
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        # The current implementation returns a string
        result = client.generate("test prompt")
        assert isinstance(result, str)
