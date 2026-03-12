import pygame
import config
from assets import get_sprite_loader


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.sprite_loader = get_sprite_loader()

    def render(self, game_state):
        self.screen.fill(config.BUS_FLOOR_COLOR)
        self._draw_bus_layout()
        self._draw_ui(game_state)
        pygame.display.flip()

    def _draw_bus_layout(self):
        bus_rect = pygame.Rect(20, 30, 280, 180)
        pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, bus_rect, 2)

        window_width = 40
        window_height = 50
        window_y = 40

        pygame.draw.rect(self.screen, config.WINDOW_COLOR, (40, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, config.WINDOW_COLOR, (140, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, config.WINDOW_COLOR, (240, window_y, window_width, window_height))

        driver_sprite = self.sprite_loader.get_sprite("driver")
        driver_lamp = self.sprite_loader.get_sprite("driver_lamp")
        if driver_sprite:
            self.screen.blit(driver_sprite, (130, 35))
        if driver_lamp:
            self.screen.blit(driver_lamp, (250, 40))

        seat_positions = [
            (35, 100, 50, 40),
            (95, 100, 50, 40),
            (175, 100, 50, 40),
            (235, 100, 50, 40),
        ]

        npc_sprites = [
            ("alex", "alex_phone", "alex_phone_glow"),
            ("maria", "maria_watch", None),
            ("emo_boy", "emo_headphones", None),
            None,
        ]

        for i, seat in enumerate(seat_positions):
            pygame.draw.rect(self.screen, config.BUS_SEAT_COLOR, seat)
            
            if i < len(npc_sprites) and npc_sprites[i]:
                npc_main, npc_prop, npc_glow = npc_sprites[i]
                npc_sprite = self.sprite_loader.get_sprite(npc_main)
                if npc_sprite:
                    self.screen.blit(npc_sprite, (seat[0] + 10, seat[1] + 5))
                
                if npc_prop:
                    prop_sprite = self.sprite_loader.get_sprite(npc_prop)
                    if prop_sprite:
                        self.screen.blit(prop_sprite, (seat[0] + 35, seat[1] + 10))
                
                if npc_glow:
                    glow_sprite = self.sprite_loader.get_sprite(npc_glow)
                    if glow_sprite:
                        self.screen.blit(glow_sprite, (seat[0] + 32, seat[1] + 5))
            else:
                passenger_rect = pygame.Rect(seat[0] + 10, seat[1] + 5, 30, 30)
                pygame.draw.rect(self.screen, config.PASSENGER_COLORS[i], passenger_rect)

        aisle_rect = pygame.Rect(150, 100, 20, 80)
        pygame.draw.rect(self.screen, (50, 45, 35), aisle_rect)

    def _draw_ui(self, game_state):
        pygame.draw.rect(self.screen, config.UI_BG_COLOR, (0, 220, 320, 20))

        time_text = f"02:{game_state.current_minute:02d}"
        loop_text = f"Loop: #{game_state.loop_count}"

        time_surface = self.font.render(time_text, True, config.UI_TEXT_COLOR)
        loop_surface = self.font.render(loop_text, True, config.UI_TEXT_COLOR)

        self.screen.blit(time_surface, (5, 222))
        self.screen.blit(loop_surface, (250, 222))
