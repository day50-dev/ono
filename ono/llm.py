import os
import requests
from typing import Optional, Dict, Any

class LLMClient:
    """
    A client for interacting with an LLM (Language Model) API.

    This class provides methods for sending requests to an LLM API and
    retrieving responses.
    """

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initializes the LLMClient.

        Args:
            api_url: The URL of the LLM API.
            api_key: The API key for accessing the LLM API.
        """
        self.api_url = api_url or os.environ.get("ONO_API_URL")
        self.api_key = api_key or os.environ.get("ONO_API_KEY")

        if not self.api_url:
            raise ValueError("LLM API URL is not set. Please set the ONO_API_URL environment variable or pass it to the LLMClient constructor.")

    def generate_text(self, prompt: str, model: Optional[str] = None, **kwargs) -> str:
        """
        Generates text using the LLM API.

        Args:
            prompt: The prompt to send to the LLM API.
            model: The model to use for generating text.
            **kwargs: Additional parameters to pass to the LLM API.

        Returns:
            The generated text.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": prompt,
            "model": model,
            **kwargs,
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        return response.json()["text"]