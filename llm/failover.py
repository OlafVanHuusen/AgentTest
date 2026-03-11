import config
from llm.ollama import OllamaClient, is_available as ollama_available
from llm.groq import GroqClient, is_available as groq_available


class LLMFailoverHandler:
    def __init__(self):
        self.ollama = OllamaClient()
        self.groq = GroqClient()
        self.primary = config.PREFERRED_LLM
        self.last_error = None

    def generate(self, prompt: str, **kwargs) -> str:
        tried = []
        errors = []

        if self.primary == "ollama":
            tried = ["ollama", "groq"]
        else:
            tried = ["groq", "ollama"]

        for provider in tried:
            try:
                if provider == "ollama" and ollama_available():
                    return self.ollama.generate(prompt, **kwargs)
                elif provider == "groq" and groq_available():
                    return self.groq.generate(prompt, **kwargs)
            except Exception as e:
                errors.append(f"{provider}: {e}")
                continue

        self.last_error = "; ".join(errors)
        raise RuntimeError(f"All LLM providers failed: {self.last_error}")

    def is_available(self) -> bool:
        return ollama_available() or groq_available()

    def get_provider_name(self) -> str:
        if self.primary == "ollama" and ollama_available():
            return "ollama"
        elif self.primary == "groq" and groq_available():
            return "groq"
        elif ollama_available():
            return "ollama"
        elif groq_available():
            return "groq"
        return "none"


_handler = None


def get_handler() -> LLMFailoverHandler:
    global _handler
    if _handler is None:
        _handler = LLMFailoverHandler()
    return _handler


def generate(prompt: str, **kwargs) -> str:
    return get_handler().generate(prompt, **kwargs)


def is_available() -> bool:
    return get_handler().is_available()
