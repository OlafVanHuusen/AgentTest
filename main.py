import logging
import pygame
import config
from game.state import GameState
from game.renderer import Renderer
from llm import ollama, groq

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_with_failover(prompt: str) -> str | None:
    error_msg = None
    
    if config.PREFERRED_LLM == "ollama" or config.PREFERRED_LLM == "auto":
        try:
            if ollama.is_available():
                logger.debug("Using Ollama for generation")
                return ollama.generate(prompt)
        except Exception as e:
            logger.warning(f"Ollama failed: {e}")
            error_msg = str(e)
    
    try:
        if groq.is_available():
            logger.debug("Falling back to Groq")
            return groq.generate(prompt)
    except Exception as e:
        logger.warning(f"Groq failed: {e}")
        error_msg = str(e)
    
    logger.error(f"Both LLM providers failed. Last error: {error_msg}")
    return None


def main():
    pygame.init()
    
    scaled_width = config.SCREEN_WIDTH * config.SCALE
    scaled_height = config.SCREEN_HEIGHT * config.SCALE
    
    screen = pygame.display.set_mode((scaled_width, scaled_height))
    pygame.display.set_caption("Timeloop Bus")
    
    game_state = GameState()
    renderer = Renderer(screen)
    
    user_input = ""
    dialogue_text = "Type your action and press ENTER..."
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input.strip():
                        action = user_input.strip()
                        dialogue_text = f"You: {action}"
                        
                        result = generate_with_failover(f"Player action: {action}")
                        
                        if result is None:
                            logger.warning("LLM failure detected, triggering lightning effect")
                            renderer.trigger_lightning_effect()
                            dialogue_text = "The time loop collapses... Everything goes white."
                            renderer.render(game_state, "", dialogue_text)
                            pygame.time.wait(1500)
                            game_state.reset_loop()
                            dialogue_text = "The bus driver looks at you. It's 2:00 AM. Again."
                        else:
                            dialogue_text = result
                            game_state.add_action(action, result)
                            game_state.advance_time()
                        
                        user_input = ""
                else:
                    if len(user_input) < 40:
                        user_input += event.unicode
        
        renderer.render(game_state, user_input, dialogue_text)
        pygame.time.wait(100)
    
    pygame.quit()


if __name__ == "__main__":
    main()
