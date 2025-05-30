# Installation

To install Ono, use pip:

```bash
pip install ono-preprocessor
```

Ono requires an OpenAI-compatible API endpoint. You can set the API URL using the `ONO_API_URL` environment variable:

```bash
export ONO_API_URL="http://localhost:8000/v1"  # vLLM
# or
export ONO_API_URL="https://api.openai.com/v1"  # OpenAI