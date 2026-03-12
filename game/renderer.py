import pygame
import config


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.input_font = pygame.font.Font(pygame.font.match_font('monospace'), 16)
        self.cursor_visible = True
        self.last_cursor_toggle = pygame.time.get_ticks()

    def render(self, game_state, user_input="", dialogue_text=""):
        self.screen.fill(config.BUS_FLOOR_COLOR)
        self._draw_bus_layout()
        self._draw_ui(game_state)
        self._draw_action_counter(game_state)
        self._draw_dialogue_box(dialogue_text)
        self._draw_input_box(user_input)
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

    def _draw_action_counter(self, game_state):
        actions_text = f"Actions: {game_state.actions_this_loop}/{game_state.max_actions_per_loop}"
        actions_surface = self.font.render(actions_text, True, config.UI_TEXT_COLOR)
        text_rect = actions_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 10))
        self.screen.blit(actions_surface, text_rect)

    def _draw_dialogue_box(self, dialogue_text):
        box_height = 60
        box_y = config.SCREEN_HEIGHT - 130
        pygame.draw.rect(self.screen, config.DIALOGUE_BG_COLOR, (5, box_y, config.SCREEN_WIDTH - 10, box_height))
        pygame.draw.rect(self.screen, config.DIALOGUE_BORDER_COLOR, (5, box_y, config.SCREEN_WIDTH - 10, box_height), 1)

        if dialogue_text:
            words = dialogue_text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                if self.input_font.size(' '.join(current_line))[0] > config.SCREEN_WIDTH - 20:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))

            for i, line in enumerate(lines[:3]):
                text_surface = self.input_font.render(line, True, config.UI_TEXT_COLOR)
                self.screen.blit(text_surface, (10, box_y + 5 + i * 18))

    def _draw_input_box(self, user_input):
        box_height = 25
        box_y = config.SCREEN_HEIGHT - 55
        pygame.draw.rect(self.screen, config.INPUT_BG_COLOR, (5, box_y, config.SCREEN_WIDTH - 10, box_height))
        pygame.draw.rect(self.screen, config.INPUT_BORDER_COLOR, (5, box_y, config.SCREEN_WIDTH - 10, box_height), 1)

        text_surface = self.input_font.render(user_input, True, config.UI_TEXT_COLOR)
        self.screen.blit(text_surface, (10, box_y + 5))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_cursor_toggle > 500:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = current_time

        if self.cursor_visible:
            text_width = self.input_font.size(user_input)[0]
            cursor_x = 10 + text_width
            pygame.draw.line(self.screen, config.INPUT_CURSOR_COLOR, (cursor_x, box_y + 3), (cursor_x, box_y + box_height - 3), 1)
