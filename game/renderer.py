"""Basic placeholder renderer for Timeloop Bus."""

import pygame
from typing import Optional

import config
from game.state import GameState


class Renderer:
    """Handles all rendering for the game."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font: Optional[pygame.font.Font] = None
        self.small_font: Optional[pygame.font.Font] = None
        self._init_fonts()

    def _init_fonts(self) -> None:
        """Initialize fonts. Uses system font as placeholder."""
        try:
            self.font = pygame.font.Font(None, 16)
            self.small_font = pygame.font.Font(None, 12)
        except Exception:
            self.font = pygame.font.SysFont("arial", 16)
            self.small_font = pygame.font.SysFont("arial", 12)

    def render(self, state: GameState) -> None:
        """Render the entire game scene."""
        self.screen.fill(config.COLORS["black"])
        self._draw_bus_interior()
        self._draw_windows()
        self._draw_driver()
        self._draw_passengers()
        self._draw_aisle()
        self._draw_ui(state)
        pygame.display.flip()

    def _draw_bus_interior(self) -> None:
        """Draw the basic bus interior."""
        bus_rect = pygame.Rect(20, 30, 280, 140)
        pygame.draw.rect(self.screen, config.COLORS["bus_floor"], bus_rect)
        pygame.draw.rect(self.screen, config.COLORS["dark_gray"], bus_rect, 2)

    def _draw_windows(self) -> None:
        """Draw the windows on the bus."""
        window_color = config.COLORS["window"]
        window_y = 40
        window_height = 50
        window_width = 30

        for x in [35, 255]:
            window_rect = pygame.Rect(x, window_y, window_width, window_height)
            pygame.draw.rect(self.screen, window_color, window_rect)
            pygame.draw.rect(self.screen, config.COLORS["light_gray"], window_rect, 1)

    def _draw_driver(self) -> None:
        """Draw the driver at the front of the bus."""
        driver_x = 130
        driver_y = 35
        driver_rect = pygame.Rect(driver_x, driver_y, 40, 35)
        pygame.draw.rect(self.screen, config.COLORS["driver"], driver_rect)

        pygame.draw.rect(self.screen, config.COLORS["ui_accent"], pygame.Rect(145, 45, 10, 8))

        if self.font:
            label = self.font.render("Driver", True, config.COLORS["light_gray"])
            self.screen.blit(label, (125, 72))

    def _draw_passengers(self) -> None:
        """Draw the passengers in their seats."""
        passengers = [
            (50, 90, config.COLORS["passenger_1"], "Alex"),
            (100, 90, config.COLORS["passenger_2"], "Maria"),
            (170, 90, config.COLORS["passenger_3"], "Kid"),
            (220, 90, config.COLORS["passenger_4"], "?"),
        ]

        for x, y, color, name in passengers:
            seat_rect = pygame.Rect(x, y, 30, 25)
            pygame.draw.rect(self.screen, config.COLORS["bus_seat"], seat_rect)
            pygame.draw.rect(self.screen, color, pygame.Rect(x + 5, y + 5, 20, 15))

            if self.small_font:
                label = self.small_font.render(name, True, config.COLORS["light_gray"])
                self.screen.blit(label, (x, y + 28))

    def _draw_aisle(self) -> None:
        """Draw the aisle in the middle of the bus."""
        aisle_rect = pygame.Rect(155, 85, 10, 70)
        pygame.draw.rect(self.screen, config.COLORS["dark_gray"], aisle_rect)

    def _draw_ui(self, state: GameState) -> None:
        """Draw the UI elements (clock, loop counter, text areas)."""
        ui_y = 175
        ui_height = 60

        ui_rect = pygame.Rect(10, ui_y, 300, ui_height)
        pygame.draw.rect(self.screen, config.COLORS["ui_bg"], ui_rect)
        pygame.draw.rect(self.screen, config.COLORS["gray"], ui_rect, 1)

        if self.font:
            time_text = f"Time: {state.get_time_string()}"
            time_surface = self.font.render(time_text, True, config.COLORS["ui_accent"])
            self.screen.blit(time_surface, (20, ui_y + 5))

            loop_text = f"Loop: #{state.loop_count}"
            loop_surface = self.font.render(loop_text, True, config.COLORS["ui_accent"])
            self.screen.blit(loop_surface, (120, ui_y + 5))

            if state.current_dialogue:
                dialogue_lines = self._wrap_text(state.current_dialogue, 280, self.small_font)
                for i, line in enumerate(dialogue_lines[:3]):
                    text_surface = self.small_font.render(line, True, config.COLORS["ui_text"])
                    self.screen.blit(text_surface, (20, ui_y + 25 + i * 12))

            input_text = f"> {state.player_input}"
            input_surface = self.font.render(input_text, True, config.COLORS["white"])
            self.screen.blit(input_surface, (20, ui_y + 45))

    def _wrap_text(self, text: str, max_width: int, font: pygame.font.Font) -> list[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
