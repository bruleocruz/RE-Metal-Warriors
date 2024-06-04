import pygame as pg


class InteractibleTile(pg.sprite.Sprite):
    def __init__(self, x, y, sprite, color='dark blue'):
        super().__init__()
        self.image = sprite
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.world_shift = pg.math.Vector2(0, 0)
    
    def update(self):
        self.rect.x += self.world_shift.x
        self.rect.y += self.world_shift.y

class NotInteractibleTile(pg.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self):
        pass
