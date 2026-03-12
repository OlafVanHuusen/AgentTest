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
                        dialogue_text = f"You: {user_input}"
                        user_input = ""
                else:
                    if len(user_input) < 40:
                        user_input += event.unicode
        
        renderer.render(game_state, user_input, dialogue_text)
        pygame.time.wait(100)
    
    pygame.quit()


if __name__ == "__main__":
    main()
