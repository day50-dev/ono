"""
Unit tests for the Ono LLM client.
"""

import pytest
from unittest.mock import Mock, patch


class TestLLMClient:
    """Test LLM client functionality."""

    def test_init_client(self):
        """Test initializing LLM client."""
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3")
        assert client.api_url == "http://localhost:11434/v1"
        assert client.model == "llama3"
        assert client.api_key is None

    def test_init_client_with_api_key(self):
        """Test initializing LLM client with API key."""
        from ono.llm import LLMClient
        client = LLMClient("http://localhost:11434/v1", "llama3", "test-key")
        assert client.api_key == "test-key"

    def test_generate_text(self):
        """Test generating text."""
        from ono.llm import LLMClient
        
        client = LLMClient("http://localhost:11434/v1", "llama3")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "mock response"}}]
            }
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = client.generate("test prompt")
            
            assert result == "mock response"

    def test_generate_with_history(self):
        """Test generating text with history."""
        from ono.llm import LLMClient
        
        client = LLMClient("http://localhost:11434/v1", "llama3")
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "How can I help?"}}]
            }
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = client.generate("test prompt", history)
            
            assert result == "How can I help?"

    def test_generate_with_options(self):
        """Test generating text with generation options."""
        from ono.llm import LLMClient
        
        client = LLMClient("http://localhost:11434/v1", "llama3")
        options = {
            "temperature": 0.7,
            "max_tokens": 100,
            "stream": False
        }
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "mock response"}}]
            }
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = client.generate("test prompt", options=options)
            
            assert result == "mock response"


class TestLLMErrors:
    """Test LLM error handling."""

    def test_api_error_handling(self):
        """Test handling of API errors."""
        from ono.llm import LLMClient
        
        client = LLMClient("http://localhost:11434/v1", "llama3")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = Exception("API error")
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            with pytest.raises(Exception):
                client.generate("test prompt")

    def test_invalid_response_handling(self):
        """Test handling of invalid API responses."""
        from ono.llm import LLMClient
        
        client = LLMClient("http://localhost:11434/v1", "llama3")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = Mock()
            mock_response.json.return_value = {}
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            with pytest.raises(Exception):
                client.generate("test prompt")
