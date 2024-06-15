import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, sprite, pos, type='', layer=0):
        super().__init__()
        self.type = type
        self.layer = layer
        
        self.image = sprite
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self):
        pass
