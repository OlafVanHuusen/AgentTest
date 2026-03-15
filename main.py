import logging
import pygame
import config
from game.state import GameState
from game.renderer import Renderer
from game.input_handler import InputHandler
from game.loop_manager import LoopManager
from assets.sound_manager import get_sound_manager

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    pygame.init()
    
    scaled_width = config.SCREEN_WIDTH * config.SCALE
    scaled_height = config.SCREEN_HEIGHT * config.SCALE
    
    screen = pygame.display.set_mode((scaled_width, scaled_height))
    pygame.display.set_caption("Timeloop Bus")
    
    clock = pygame.time.Clock()
    
    sound_manager = get_sound_manager()
    sound_manager.load_sound('loop_reset', 'bus_engine.wav')
    sound_manager.load_sound('thunder', 'thunder.wav')
    sound_manager.load_music('ambient', 'ambient.wav')
    
    game_state = GameState()
    renderer = Renderer(screen)
    input_handler = InputHandler(screen)
    loop_manager = LoopManager(screen, sound_manager)
    
    if sound_manager.enabled:
        sound_manager.play_music('ambient')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    renderer.toggle_debug_overlay()
            else:
                input_handler.handle_event(event, game_state, loop_manager)
        
        if hasattr(game_state, 'llm_failed') and game_state.llm_failed:
            game_state.llm_failed = False
            renderer.trigger_lightning_effect()
            loop_manager.trigger_loop_reset(game_state)
        
        loop_manager.update(game_state)
        
        renderer.render(game_state)
        input_handler.render(game_state)
        
        if loop_manager.is_effect_active():
            loop_manager.render_effect()
        
        clock.tick(60)
    
    sound_manager.stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
