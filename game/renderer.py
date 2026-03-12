import pygame
import config
from assets import get_sprite_loader


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.input_font = pygame.font.Font(pygame.font.match_font('monospace'), 16)
        self.cursor_visible = True
        self.last_cursor_toggle = pygame.time.get_ticks()
        self.sprite_loader = get_sprite_loader()

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

        self._draw_driver_cockpit()
        self._draw_windows()
        self._draw_seats()
        self._draw_aisle()
        self._draw_bathroom_door()

    def _draw_driver_cockpit(self):
        cockpit_rect = pygame.Rect(100, 35, 120, 30)
        pygame.draw.rect(self.screen, config.DRIVER_COCKPIT_COLOR, cockpit_rect)
        pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, cockpit_rect, 2)

        steering_rect = pygame.Rect(155, 40, 10, 20)
        pygame.draw.rect(self.screen, config.STEERING_WHEEL_COLOR, steering_rect)

        driver_sprite = self.sprite_loader.get_sprite("driver")
        if driver_sprite:
            self.screen.blit(driver_sprite, (130, 35))
        
        driver_lamp = self.sprite_loader.get_sprite("driver_lamp")
        if driver_lamp:
            self.screen.blit(driver_lamp, (250, 40))

    def _draw_windows(self):
        window_width = 35
        window_height = 45
        window_y = 75

        left_windows = [(30, window_y), (75, window_y)]
        right_windows = [(205, window_y), (250, window_y)]

        for wx, wy in left_windows + right_windows:
            pygame.draw.rect(self.screen, config.WINDOW_COLOR, (wx, wy, window_width, window_height))
            pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, (wx, wy, window_width, window_height), 1)

    def _draw_seats(self):
        seat_width = 45
        seat_height = 35
        row1_y = 130
        row2_y = 170

        left_seats_row1 = [(30, row1_y), (80, row1_y)]
        right_seats_row1 = [(195, row1_y), (245, row1_y)]
        left_seats_row2 = [(30, row2_y), (80, row2_y)]
        right_seats_row2 = [(195, row2_y), (245, row2_y)]

        all_seats = left_seats_row1 + right_seats_row1 + left_seats_row2 + right_seats_row2

        for sx, sy in all_seats:
            pygame.draw.rect(self.screen, config.BUS_SEAT_COLOR, (sx, sy, seat_width, seat_height))
            pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, (sx, sy, seat_width, seat_height), 1)

        npc_positions = [
            (0, "alex", "alex_phone", "alex_phone_glow"),
            (1, "maria", "maria_watch", None),
            (2, "emo_boy", "emo_headphones", None),
            (5, None, None, None),
        ]

        for seat_idx, npc_main, npc_prop, npc_glow in npc_positions:
            if seat_idx < len(all_seats):
                sx, sy = all_seats[seat_idx]
                
                if npc_main:
                    npc_sprite = self.sprite_loader.get_sprite(npc_main)
                    if npc_sprite:
                        self.screen.blit(npc_sprite, (sx + 8, sy + 3))
                    
                    if npc_prop:
                        prop_sprite = self.sprite_loader.get_sprite(npc_prop)
                        if prop_sprite:
                            self.screen.blit(prop_sprite, (sx + 28, sy + 8))
                    
                    if npc_glow:
                        glow_sprite = self.sprite_loader.get_sprite(npc_glow)
                        if glow_sprite:
                            self.screen.blit(glow_sprite, (sx + 25, sy + 3))
                else:
                    passenger_rect = pygame.Rect(sx + 8, sy + 3, 28, 28)
                    pygame.draw.rect(self.screen, config.EMPTY_SEAT_COLOR, passenger_rect)

    def _draw_aisle(self):
        aisle_x = 145
        aisle_y = 130
        aisle_width = 30
        aisle_height = 70
        
        pygame.draw.rect(self.screen, config.AISLE_COLOR, (aisle_x, aisle_y, aisle_width, aisle_height))

    def _draw_bathroom_door(self):
        door_width = 25
        door_height = 35
        door_x = 270
        door_y = 175
        
        pygame.draw.rect(self.screen, config.BATHROOM_DOOR_COLOR, (door_x, door_y, door_width, door_height))
        pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, (door_x, door_y, door_width, door_height), 1)
        
        handle_x = door_x + 3
        handle_y = door_y + 15
        pygame.draw.rect(self.screen, config.DOOR_HANDLE_COLOR, (handle_x, handle_y, 3, 6))

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

    def trigger_lightning_effect(self):
        flash_count = 3
        for _ in range(flash_count):
            self.screen.fill((255, 255, 255))
            pygame.display.flip()
            pygame.time.wait(50)
            self.screen.fill(config.BUS_FLOOR_COLOR)
            pygame.display.flip()
            pygame.time.wait(50)
