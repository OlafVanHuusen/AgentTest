import pygame
from pathlib import Path

SPRITE_SCALE = 3


def create_surface_from_array(pixel_array, scale=SPRITE_SCALE):
    height = len(pixel_array)
    width = len(pixel_array[0]) if height > 0 else 0
    
    surface = pygame.Surface((width * scale, height * scale), pygame.SRCALPHA)
    
    for y, row in enumerate(pixel_array):
        for x, color in enumerate(row):
            if color != 0:
                pygame.draw.rect(
                    surface, 
                    color, 
                    (x * scale, y * scale, scale, scale)
                )
    
    return surface


class SpriteLoader:
    def __init__(self):
        self.sprites = {}
        self._load_sprites()
    
    def _load_sprites(self):
        from assets.sprites import driver, alex, maria, emo_boy
        
        self.sprites["driver"] = create_surface_from_array(driver.DRIVER_SPRITE)
        self.sprites["driver_lamp"] = create_surface_from_array(driver.DRIVER_LAMP)
        
        self.sprites["alex"] = create_surface_from_array(alex.ALEX_SPRITE)
        self.sprites["alex_phone"] = create_surface_from_array(alex.ALEX_PHONE)
        self.sprites["alex_phone_glow"] = create_surface_from_array(alex.ALEX_PHONE_GLOW)
        
        self.sprites["maria"] = create_surface_from_array(maria.MARIA_SPRITE)
        self.sprites["maria_watch"] = create_surface_from_array(maria.MARIA_WATCH)
        
        self.sprites["emo_boy"] = create_surface_from_array(emo_boy.EMO_BOY_SPRITE)
        self.sprites["emo_headphones"] = create_surface_from_array(emo_boy.EMO_HEADPHONES)
    
    def get_sprite(self, name):
        return self.sprites.get(name)


_sprite_loader = None


def get_sprite_loader():
    global _sprite_loader
    if _sprite_loader is None:
        _sprite_loader = SpriteLoader()
    return _sprite_loader
