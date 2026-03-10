"""Main entry point for Timeloop Bus."""

import pygame
import sys

import config
from game.state import GameState
from game.renderer import Renderer


def main():
    """Main game loop."""
    pygame.init()

    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH * config.SCALE, config.SCREEN_HEIGHT * config.SCALE)
    )
    pygame.display.set_caption("Timeloop Bus")
    screen.fill(config.COLORS["black"])

    game_state = GameState()
    renderer = Renderer(screen)

    clock = pygame.time.Clock()
    running = True

    game_state.set_dialogue("You are trapped on a greyhound bus. It's 2 AM. The driver won't speak. The passengers are sleeping. Something is wrong.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    game_state.player_input = game_state.player_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if game_state.player_input.strip():
                        game_state.add_action(game_state.player_input)
                        game_state.advance_time()
                        game_state.set_dialogue(f"You: {game_state.player_input}")
                        game_state.player_input = ""

                        if game_state.should_reset():
                            game_state.reset_loop()
                            game_state.set_dialogue("The world fades... You wake up on the bus again.")

        renderer.render(game_state)
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
