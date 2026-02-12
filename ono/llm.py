import httpx


class LLMClient:
    def __init__(self, api_url: str, model: str, api_key: str = None):
        self.api_url = api_url
        self.model = model
        self.api_key = api_key

    def generate(self, prompt: str, history: list = None, options: dict = None):
        return f"generated response for: {prompt}"
