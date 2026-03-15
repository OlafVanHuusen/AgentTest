from typing import Optional, Any
from .base import LLMClient
from . import ollama, groq
import config


class FailoverHandler:
    def __init__(self, preferred: Optional[str] = None):
        if preferred is None:
            preferred = getattr(config, 'PREFERRED_LLM', 'ollama')
        self.preferred = preferred
        self._primary: Any = None
        self._fallback: Any = None
        self._web_mode = getattr(config, 'WEB_MODE', False)

    def _get_clients(self):
        if self._web_mode:
            self._primary = groq
            self._fallback = None
            return

        if self.preferred == "groq":
            primary_name = "groq"
            fallback_name = "ollama"
        else:
            primary_name = "ollama"
            fallback_name = "groq"

        if primary_name == "groq":
            self._primary = groq
            self._fallback = ollama
        else:
            self._primary = ollama
            self._fallback = groq

    def generate(self, prompt: str, **kwargs) -> str:
        self._get_clients()

        if self._web_mode:
            if self._primary.is_available():
                try:
                    return self._primary.generate(prompt, **kwargs)
                except Exception as e:
                    raise RuntimeError(f"Groq API not available: {e}")
            raise RuntimeError("Groq API not available in web mode. Please set GROQ_API_KEY.")

        if self._primary.is_available():
            try:
                return self._primary.generate(prompt, **kwargs)
            except Exception:
                pass

        if self._fallback and self._fallback.is_available():
            try:
                return self._fallback.generate(prompt, **kwargs)
            except Exception:
                pass

        raise RuntimeError("No LLM providers available")

    def is_available(self) -> bool:
        self._get_clients()

        if self._web_mode:
            return self._primary.is_available()

        return self._primary.is_available() or (self._fallback is not None and self._fallback.is_available())


_handler = None


def get_handler() -> FailoverHandler:
    global _handler
    if _handler is None:
        _handler = FailoverHandler()
    return _handler


def generate(prompt: str, **kwargs) -> str:
    return get_handler().generate(prompt, **kwargs)


def is_available() -> bool:
    return get_handler().is_available()