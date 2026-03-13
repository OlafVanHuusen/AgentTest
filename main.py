import pygame
import config
from game.state import GameState
from game.renderer import Renderer
from game.input_handler import InputHandler
from game.loop_manager import LoopManager


def main():
    pygame.init()
    
    scaled_width = config.SCREEN_WIDTH * config.SCALE
    scaled_height = config.SCREEN_HEIGHT * config.SCALE
    
    screen = pygame.display.set_mode((scaled_width, scaled_height))
    pygame.display.set_caption("Timeloop Bus")
    
    game_state = GameState()
    renderer = Renderer(screen)
    input_handler = InputHandler(screen)
    loop_manager = LoopManager(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                input_handler.handle_event(event, game_state, loop_manager)
        
        loop_manager.update(game_state)
        
        renderer.render(game_state)
        input_handler.render(game_state)
        
        if loop_manager.is_effect_active():
            loop_manager.render_effect()
        
        pygame.time.wait(50)
    
    pygame.quit()


if __name__ == "__main__":
    main()
