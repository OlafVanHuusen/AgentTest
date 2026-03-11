import requests
import config


class OllamaClient:
    def __init__(self, url: str = None, model: str = None):
        self.url = url or config.OLLAMA_URL
        self.model = model or config.OLLAMA_MODEL
        self.generate_endpoint = f"{self.url}/api/generate"

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise RuntimeError("Ollama is not available. Check server and connectivity.")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "num_predict": kwargs.get("max_tokens", 512),
            }
        }

        try:
            response = requests.post(
                self.generate_endpoint,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


_client = None


def get_client() -> OllamaClient:
    global _client
    if _client is None:
        _client = OllamaClient()
    return _client


def generate(prompt: str, **kwargs) -> str:
    return get_client().generate(prompt, **kwargs)


def is_available() -> bool:
    return get_client().is_available()
