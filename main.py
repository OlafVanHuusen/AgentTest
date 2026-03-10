import pygame
import config
from game.state import GameState
from game.renderer import Renderer


def main():
    pygame.init()
    
    scaled_width = config.SCREEN_WIDTH * config.SCALE
    scaled_height = config.SCREEN_HEIGHT * config.SCALE
    
    screen = pygame.display.set_mode((scaled_width, scaled_height))
    pygame.display.set_caption("Timeloop Bus")
    
    game_state = GameState()
    renderer = Renderer(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        renderer.render(game_state)
        pygame.time.wait(100)
    
    pygame.quit()


if __name__ == "__main__":
    main()
