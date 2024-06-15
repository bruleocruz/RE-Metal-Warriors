import pygame as pg
from random import randint


class Shoot1(pg.sprite.Sprite):
    def __init__(self, entity, sprite, pos, front):
        super().__init__()

        self.entity = entity
        self.delay = 0

        self.damage = 10
        self.front = front
    
        self.image = sprite
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self):
        if self.front:
            self.rect.x += 16
            #self.rect.y += randint(-5, 5)
        else:
            self.rect.x -= 16
            #self.rect.y += randint(-5, 5)