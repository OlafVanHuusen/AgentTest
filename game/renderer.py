import pygame
import config
from assets import get_sprite_loader


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.sprite_loader = get_sprite_loader()
        self.debug_overlay = False
        self.debug_font = pygame.font.Font(None, 14)

    def render(self, game_state):
        self.screen.fill(config.BUS_FLOOR_COLOR)
        self._draw_bus_layout()
        self._draw_visual_states(game_state.world_changes)
        self._draw_ui(game_state)
        
        if self.debug_overlay:
            self._draw_debug_overlay(game_state)
        
        pygame.display.flip()

    def toggle_debug_overlay(self):
        self.debug_overlay = not self.debug_overlay

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

    def _draw_visual_states(self, world_changes):
        if not world_changes:
            return
        
        for change_key, change_data in world_changes.items():
            if change_key.startswith("window_broken"):
                self._draw_broken_window(change_data)
            elif change_key.startswith("blood_stain"):
                self._draw_blood_stain(change_data)
            elif change_key.startswith("item_moved"):
                self._draw_item_moved(change_data)
            elif change_key.startswith("item_changed"):
                self._draw_item_changed(change_data)
            elif change_key.startswith("fire_on_bus"):
                self._draw_fire(change_data)

    def _draw_broken_window(self, data):
        window_index = data.get("window_index", 0)
        window_positions = {
            0: (30, 75),
            1: (75, 75),
            2: (205, 75),
            3: (250, 75),
        }
        wx, wy = window_positions.get(window_index, (30, 75))
        
        pygame.draw.rect(self.screen, config.BROKEN_WINDOW_COLOR, (wx, wy, 35, 45))
        pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, (wx, wy, 35, 45), 1)
        
        crack_lines = [
            ((wx + 5, wy + 5), (wx + 20, wy + 25)),
            ((wx + 20, wy + 25), (wx + 30, wy + 10)),
            ((wx + 10, wy + 30), (wx + 25, wy + 40)),
        ]
        for start, end in crack_lines:
            pygame.draw.line(self.screen, config.CRACK_COLOR, start, end, 1)

    def _draw_blood_stain(self, data):
        x = data.get("x", 0)
        y = data.get("y", 0)
        size = data.get("size", 20)
        
        stain_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(stain_surface, (*config.BLOOD_STAIN_COLOR, config.BLOOD_STAIN_ALPHA), (size // 2, size // 2), size // 2)
        self.screen.blit(stain_surface, (x, y))

    def _draw_item_moved(self, data):
        pass

    def _draw_item_changed(self, data):
        pass

    def _draw_fire(self, data):
        x = data.get("x", 0)
        y = data.get("y", 0)
        intensity = data.get("intensity", 1)
        
        fire_colors = [(255, 100, 0), (255, 50, 0), (200, 0, 0)]
        for i, color in enumerate(fire_colors):
            size = 15 - i * 3
            offset_y = i * 5
            pygame.draw.circle(self.screen, color, (x + 10, y + offset_y), size * intensity // 2)

    def _draw_ui(self, game_state):
        pygame.draw.rect(self.screen, config.UI_BG_COLOR, (0, 220, 320, 20))

        time_text = f"02:{game_state.current_minute:02d}"
        loop_text = f"Loop: #{game_state.loop_count}"

        time_surface = self.font.render(time_text, True, config.UI_TEXT_COLOR)
        loop_surface = self.font.render(loop_text, True, config.UI_TEXT_COLOR)

        self.screen.blit(time_surface, (5, 222))
        self.screen.blit(loop_surface, (250, 222))

    def _draw_debug_overlay(self, game_state):
        overlay_bg = pygame.Surface((150, 60))
        overlay_bg.set_alpha(200)
        overlay_bg.fill((0, 0, 0))
        self.screen.blit(overlay_bg, (5, 5))
        
        debug_lines = [
            f"DEBUG MODE",
            f"Loop: #{game_state.loop_count}",
            f"Minute: {game_state.current_minute}",
            f"Actions: {len(game_state.actions_taken)}"
        ]
        
        for i, line in enumerate(debug_lines):
            text_surface = self.debug_font.render(line, True, (0, 255, 0))
            self.screen.blit(text_surface, (10, 8 + i * 12))
