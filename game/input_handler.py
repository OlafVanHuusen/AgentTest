import pygame


class InputHandler:
    def __init__(self):
        self.input_text = ""
        self.is_inputting = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 100

    def handle_event(self, event) -> str:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    text = self.input_text.strip()
                    self.input_text = ""
                    self.is_inputting = False
                    return text
                return ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.input_text = ""
                self.is_inputting = False
            elif event.key == pygame.K_SPACE:
                if len(self.input_text) < self.max_length:
                    self.input_text += " "
            elif event.unicode and len(self.input_text) < self.max_length:
                if event.unicode.isprintable():
                    self.input_text += event.unicode
        
        return ""

    def start_input(self):
        self.is_inputting = True
        self.input_text = ""

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= 500:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def get_display_text(self) -> str:
        if self.cursor_visible and self.is_inputting:
            return self.input_text + "|"
        return self.input_text
