import pygame
import config
from game.state import GameState
from game.renderer import Renderer
from game.input_handler import InputHandler
from llm import get_handler, PromptBuilder, is_available as llm_available


def main():
    pygame.init()
    
    scaled_width = config.SCREEN_WIDTH * config.SCALE
    scaled_height = config.SCREEN_HEIGHT * config.SCALE
    
    screen = pygame.display.set_mode((scaled_width, scaled_height))
    pygame.display.set_caption("Timeloop Bus")
    
    game_state = GameState()
    renderer = Renderer(screen)
    input_handler = InputHandler()
    prompt_builder = PromptBuilder()
    llm_handler = get_handler()
    
    if llm_available():
        renderer.set_provider_status(f"LLM: {llm_handler.get_provider_name()}")
    else:
        renderer.set_provider_status("LLM: unavailable")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if input_handler.is_inputting:
                action = input_handler.handle_event(event)
                if action:
                    if game_state.actions:
                        prompt = prompt_builder.build_action_prompt(action, game_state)
                    else:
                        prompt = prompt_builder.build_first_action_prompt(action)
                    
                    try:
                        response = llm_handler.generate(prompt)
                        renderer.set_dialogue(response)
                        game_state.add_action(action, response)
                        game_state.advance_time()
                    except RuntimeError as e:
                        renderer.set_dialogue(f"LLM Error: {e}")
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_t:
                        input_handler.start_input()
                        renderer.clear_dialogue()
        
        input_handler.update(dt)
        renderer.render(game_state, input_handler)
    
    pygame.quit()


if __name__ == "__main__":
    main()
