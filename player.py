import pygame as pg
from pygame.image import load
from config import debug

class Nitro(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.screen = pg.display.get_surface()
        nitro_path = 'sprites/chars/nitro/'
        self.sprites = {'walk': [pg.transform.scale(load(nitro_path + 'walk/00.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/01.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/02.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/03.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/04.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/05.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/06.png'), (128, 128)),
                                 pg.transform.scale(load(nitro_path + 'walk/07.png'), (128, 128))]}
        self.state = 'walk'
        self.index = 0

        # PHYSICAL
        self.axis = pg.math.Vector2(0, 0)
        self.speed_limit = [-12, 12]
        self.gravity_level = 1
        self.gravity_limit = [-24, 24]
        self.stand = True
        self.face_right = True

        # COLLIDE STATES;
        self.on_ceiling = False
        self.on_ground = False
        self.on_left = False
        self.on_right = False

        # VISUAL
        self.image = self.sprites[self.state][self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def command_button(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            self.rect.center = pg.mouse.get_pos()

        if self.on_ground:
            if keys[pg.K_DOWN]:
                self.axis.y = -24
        if keys[pg.K_a]:
            self.axis.x -= 0.5
            self.face_right = False
        elif keys[pg.K_d]:
            self.axis.x += 0.5
            self.face_right = True
        else:
            self.accel_reset()
        
        self.movement_control_limit()
    
    # TO NOT SURPASS SPEED AND GRAVTY LIMITS;
    def movement_control_limit(self):
        if self.axis.x <= self.speed_limit[0]:
            self.axis.x = self.speed_limit[0]
        elif self.axis.x >= self.speed_limit[1]:
            self.axis.x = self.speed_limit[1]
        if self.axis.y <= self.gravity_limit[0]:
            self.axis.y = self.gravity_limit[0]
        elif self.axis.y >= self.gravity_limit[1]:
            self.axis.y = self.gravity_limit[1]

    # BRING SPEED TO 0 WHEN THERES NO BUTTONS GET PRESSED;
    def accel_reset(self):
        if self.axis.x < 0:
            self.axis.x += 0.5
        elif self.axis.x > 0:
            self.axis.x -= 0.5
    
    # APPLYING GRAVITY;
    def gravity(self):
        self.axis.y += self.gravity_level
    
    def apply_gravity(self):
        self.rect.y += int(self.axis.y)

    #APPLYING ACCEL;
    def apply_movement(self):
        self.rect.x += int(self.axis.x)
    
    def state_config(self):
        if not self.stand:
            if self.state == 'walk':
                if self.index >= 7:
                    self.index = 0
                else:
                    self.index += 0.4
    
    def animation(self):
        # IMAGE CONFIG;
        if self.face_right:
            self.image = self.sprites[self.state][int(self.index)]
        else:
             self.image = pg.transform.flip(self.sprites[self.state][int(self.index)], True, False)

        # RECT CONFIG;
        if self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self):
        self.state_config()
        self.animation()
