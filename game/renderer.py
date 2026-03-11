import pygame
import config
import textwrap


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.dialogue = ""
        self.dialogue_visible = False
        self.provider_status = ""

    def render(self, game_state, input_handler=None):
        self.screen.fill(config.BUS_FLOOR_COLOR)
        self._draw_bus_layout()
        self._draw_ui(game_state)
        
        if self.dialogue_visible and self.dialogue:
            self._draw_dialogue_box()
        
        if input_handler and input_handler.is_inputting:
            self._draw_input_box(input_handler.get_display_text())
        
        pygame.display.flip()

    def set_dialogue(self, text: str):
        self.dialogue = text
        self.dialogue_visible = True

    def clear_dialogue(self):
        self.dialogue = ""
        self.dialogue_visible = False

    def set_provider_status(self, status: str):
        self.provider_status = status

    def _draw_bus_layout(self):
        bus_rect = pygame.Rect(20, 30, 280, 180)
        pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, bus_rect, 2)

        window_width = 40
        window_height = 50
        window_y = 40

        pygame.draw.rect(self.screen, config.WINDOW_COLOR, (40, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, config.WINDOW_COLOR, (140, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, config.WINDOW_COLOR, (240, window_y, window_width, window_height))

        driver_rect = pygame.Rect(110, 35, 100, 30)
        pygame.draw.rect(self.screen, config.DRIVER_COLOR, driver_rect)

        seat_positions = [
            (35, 100, 50, 40),
            (95, 100, 50, 40),
            (175, 100, 50, 40),
            (235, 100, 50, 40),
        ]

        for i, seat in enumerate(seat_positions):
            pygame.draw.rect(self.screen, config.BUS_SEAT_COLOR, seat)
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

        if self.provider_status:
            status_surface = self.font.render(self.provider_status, True, (150, 150, 150))
            self.screen.blit(status_surface, (100, 222))

    def _draw_dialogue_box(self):
        box_rect = pygame.Rect(20, 140, 280, 70)
        pygame.draw.rect(self.screen, config.UI_BG_COLOR, box_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), box_rect, 1)

        wrapper = textwrap.TextWrapper(width=38)
        lines = wrapper.wrap(self.dialogue)
        
        y_offset = box_rect.y + 5
        for line in lines[:3]:
            text_surface = self.font.render(line, True, config.UI_TEXT_COLOR)
            self.screen.blit(text_surface, (box_rect.x + 5, y_offset))
            y_offset += 18

    def _draw_input_box(self, text: str):
        box_rect = pygame.Rect(20, 215, 280, 20)
        pygame.draw.rect(self.screen, (20, 20, 20), box_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), box_rect, 1)

        text_surface = self.font.render(text, True, config.UI_TEXT_COLOR)
        self.screen.blit(text_surface, (box_rect.x + 5, box_rect.y + 2))
