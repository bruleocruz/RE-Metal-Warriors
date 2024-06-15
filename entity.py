import pygame as pg
from config import *


class Nitro(pg.sprite.Sprite):
    def load_sprites():
        sprites = LOAD_SPRITES('sprites/chars/nitro')
        return sprites

    def __init__(self, type='', pos=(0, 0)):
        super().__init__()
        self.type = type
        self.sprites = Nitro.load_sprites()
        self.state = 'walk'
        self.index = 0
        self.frame_skip = 0

        # PHYSIC;
        self.movement = pg.math.Vector2(0, 0)
        self.x_limit = [-8, 8]
        self.y_limit = [-16, 16]
        self.gravity = 1

        # STUFFS;
        self.on_left = False
        self.on_right = False
        self.on_ceiling = False
        self.on_ground = False
        self.stand = True

        # ANIMATION;
        self.image = self.sprites[self.state][self.index]
        self.rect = self.image.get_rect(topleft=(pos))
        self.face_right = True

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_DOWN]:
            self.gravity = -16

        if keys[pg.K_a]:
            self.movement.x -= 1
            self.face_right = False
        elif keys[pg.K_d]:
            self.movement.x += 1
            self.face_right = True
        else:
            self.reset_speed()
        
        self.speed_limit()
    
    def reset_speed(self):
        if self.movement.x < 0:
            self.movement.x += 0.5
        if self.movement.x > 0:
            self.movement.x -= 0.5
    
    def speed_limit(self):
        if self.movement.x < self.x_limit[0]:
            self.movement.x = self.x_limit[0]
        if self.movement.x > self.x_limit[1]:
            self.movement.x = self.x_limit[1]
        if self.movement.y < self.y_limit[0]:
            self.movement.y = self.y_limit[0]
        if self.movement.y > self.y_limit[1]:
            self.movement.y = self.y_limit[1]

    def apply_movement_x(self):
        self.rect.x += int(self.movement.x)
    
    def apply_gravity(self):
        self.gravity += 1
    
    def apply_movement_y(self):
        self.movement.y = self.gravity
        self.speed_limit()
        self.rect.y += int(self.movement.y)
    
    def state_config(self):
        if self.movement.x != 0:
            if self.state == 'walk':
                if self.index >= len(self.sprites[self.state]) - 1:
                    self.index = 0
                else:
                    self.index += 0.4
    
    def animation(self):
        # IMAGE CONFIG;
        if not self.face_right:
            self.image = pg.transform.flip(self.sprites[self.state][int(self.index)], True, False)
        else:
            self.image = self.sprites[self.state][int(self.index)]
        
        # RECT CONFIG;
        if self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        if self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
    
    def update(self):
        self.input()
        self.state_config()
        self.animation()
