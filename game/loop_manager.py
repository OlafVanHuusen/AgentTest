import pygame
import random


class LoopManager:
    def __init__(self, screen):
        self.screen = screen
        self.effect_active = False
        self.effect_timer = 0
        self.effect_duration = 60
        self.effect_type = None
        self.original_surface = None

    def check_and_trigger_loop_reset(self, game_state):
        if game_state.actions_this_loop >= game_state.max_actions_per_loop and not game_state.game_over:
            self.trigger_loop_reset(game_state)
            return True
        return False

    def trigger_loop_reset(self, game_state):
        self.effect_active = True
        self.effect_timer = 0
        self.effect_type = "loop_reset"
        self.original_surface = self.screen.copy()

    def update(self, game_state):
        if self.effect_active:
            self.effect_timer += 1
            if self.effect_timer >= self.effect_duration:
                self._perform_reset(game_state)
                self.effect_active = False
                self.effect_timer = 0
                self.original_surface = None

    def render_effect(self):
        if not self.effect_active or self.original_surface is None:
            return

        progress = self.effect_timer / self.effect_duration

        if progress < 0.2:
            self._render_glitch_effect(progress)
        elif progress < 0.5:
            self._render_flash_effect(progress)
        elif progress < 0.8:
            self._render_fade_to_white(progress)
        else:
            self._render_fade_from_white(progress)

        pygame.display.flip()

    def _render_glitch_effect(self, progress):
        glitch_intensity = int(20 * (1 - progress / 0.2))
        for _ in range(glitch_intensity):
            x = random.randint(0, self.screen.get_width() - 50)
            y = random.randint(0, self.screen.get_height() - 50)
            width = random.randint(10, 50)
            height = random.randint(2, 10)
            color = (
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(200, 255)
            )
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        if random.random() < 0.3:
            offset = random.randint(-5, 5)
            temp_surface = self.original_surface.copy()
            self.screen.blit(temp_surface, (offset, 0))

    def _render_flash_effect(self, progress):
        flash_alpha = int(100 * ((progress - 0.2) / 0.3))
        flash_surface = pygame.Surface(self.screen.get_size())
        flash_surface.fill((255, 255, 255))
        flash_surface.set_alpha(flash_alpha)
        self.screen.blit(self.original_surface, (0, 0))
        self.screen.blit(flash_surface, (0, 0))

    def _render_fade_to_white(self, progress):
        fade_progress = (progress - 0.5) / 0.3
        fade_alpha = int(255 * fade_progress)
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((255, 255, 255))
        fade_surface.set_alpha(fade_alpha)
        self.screen.blit(fade_surface, (0, 0))

    def _render_fade_from_white(self, progress):
        fade_progress = (progress - 0.8) / 0.2
        fade_alpha = int(255 * (1 - fade_progress))
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((255, 255, 255))
        fade_surface.set_alpha(fade_alpha)
        self.screen.fill((0, 0, 0))
        self.screen.blit(fade_surface, (0, 0))

    def _perform_reset(self, game_state):
        game_state.reset_loop()

    def is_effect_active(self):
        return self.effect_active
