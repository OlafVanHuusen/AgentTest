import os
import requests

import config


class GroqClient:
    def __init__(self, api_key: str = None, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY") or config.GROQ_API_KEY
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.chat_endpoint = f"{self.base_url}/chat/completions"

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise RuntimeError("Groq API is not available. Check API key and connectivity.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 512)
        }

        try:
            response = requests.post(
                self.chat_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Groq API request failed: {e}")

    def is_available(self) -> bool:
        if not self.api_key:
            return False

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 1
            }
            response = requests.post(
                self.chat_endpoint,
                headers=headers,
                json=payload,
                timeout=10
            )
            return response.status_code < 500
        except requests.exceptions.RequestException:
            return False


_client = None


def get_client() -> GroqClient:
    global _client
    if _client is None:
        _client = GroqClient()
    return _client


def generate(prompt: str, **kwargs) -> str:
    return get_client().generate(prompt, **kwargs)


def is_available() -> bool:
    return get_client().is_available()
