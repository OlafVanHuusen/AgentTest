import logging

import config
from llm import ollama
from llm import groq

logger = logging.getLogger(__name__)


def lightning_effect():
    """Trigger visual lightning effect for LLM failure."""
    logger.warning("LLM FAILURE: Triggering lightning effect")
    print("[VISUAL] Lightning effect triggered - screen flash")


def generate_with_failover(prompt: str, **kwargs) -> str:
    """
    Try Ollama first, then fallback to Groq.
    If both fail, trigger lightning effect and reset loop.
    
    Args:
        prompt: The prompt to send to the LLM
        **kwargs: Additional arguments passed to the LLM
        
    Returns:
        The generated text response
        
    Raises:
        RuntimeError: If both providers fail
    """
    tried_ollama = False
    tried_groq = False
    
    if config.PREFERRED_LLM == "ollama":
        tried_ollama = True
        logger.info("Attempting Ollama first...")
        try:
            if ollama.is_available():
                result = ollama.generate(prompt, **kwargs)
                logger.info("Ollama succeeded")
                return result
            else:
                logger.warning("Ollama not available")
        except Exception as e:
            logger.warning(f"Ollama failed: {e}")
        
        tried_groq = True
        logger.info("Falling back to Groq...")
        try:
            if groq.is_available():
                result = groq.generate(prompt, **kwargs)
                logger.info("Groq succeeded (fallback)")
                return result
            else:
                logger.warning("Groq not available")
        except Exception as e:
            logger.warning(f"Groq failed: {e}")
    else:
        tried_groq = True
        logger.info("Attempting Groq first...")
        try:
            if groq.is_available():
                result = groq.generate(prompt, **kwargs)
                logger.info("Groq succeeded")
                return result
            else:
                logger.warning("Groq not available")
        except Exception as e:
            logger.warning(f"Groq failed: {e}")
        
        tried_ollama = True
        logger.info("Falling back to Ollama...")
        try:
            if ollama.is_available():
                result = ollama.generate(prompt, **kwargs)
                logger.info("Ollama succeeded (fallback)")
                return result
            else:
                logger.warning("Ollama not available")
        except Exception as e:
            logger.warning(f"Ollama failed: {e}")
    
    logger.error(f"All LLM providers failed. Ollama tried: {tried_ollama}, Groq tried: {tried_groq}")
    lightning_effect()
    raise RuntimeError("All LLM providers failed - loop reset triggered")


def reset_loop(game_state):
    """
    Reset the game loop after LLM failure.
    
    Args:
        game_state: The current game state to reset
    """
    logger.warning("LLM FAILURE: Resetting loop")
    game_state.reset_loop()
