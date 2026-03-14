import os
import config


class SoundManager:
    def __init__(self, sounds_dir=None):
        self.enabled = getattr(config, 'ENABLE_SOUND', True)
        self.sounds = {}
        self.music = {}
        self._initialized = False
        
        if sounds_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sounds_dir = os.path.join(base_dir, 'assets', 'sounds')
        self.sounds_dir = sounds_dir
        
    def _init_pygame_mixer(self):
        if self._initialized:
            return
        try:
            import pygame
            pygame.mixer.init()
            self._initialized = True
        except Exception:
            self.enabled = False
            
    def load_sound(self, name, filename=None):
        if not self.enabled:
            return
        if filename is None:
            filename = f"{name}.ogg"
        filepath = os.path.join(self.sounds_dir, filename)
        if not os.path.exists(filepath):
            return
        try:
            import pygame
            self._init_pygame_mixer()
            self.sounds[name] = pygame.mixer.Sound(filepath)
        except Exception:
            pass
            
    def load_music(self, name, filename=None):
        if not self.enabled:
            return
        if filename is None:
            filename = f"{name}.ogg"
        filepath = os.path.join(self.sounds_dir, filename)
        if not os.path.exists(filepath):
            return
        try:
            import pygame
            self._init_pygame_mixer()
            self.music[name] = filepath
        except Exception:
            pass
            
    def play_sound(self, name):
        if not self.enabled or name not in self.sounds:
            return
        try:
            self.sounds[name].play()
        except Exception:
            pass
            
    def play_music(self, name, loops=-1):
        if not self.enabled or name not in self.music:
            return
        try:
            import pygame
            pygame.mixer.music.load(self.music[name])
            pygame.mixer.music.play(loops)
        except Exception:
            pass
            
    def stop_music(self):
        if not self.enabled:
            return
        try:
            import pygame
            pygame.mixer.music.stop()
        except Exception:
            pass
            
    def fadeout_music(self, ms=500):
        if not self.enabled:
            return
        try:
            import pygame
            pygame.mixer.music.fadeout(ms)
        except Exception:
            pass


_sound_manager = None


def get_sound_manager() -> SoundManager:
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
