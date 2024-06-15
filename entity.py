import pygame as pg
from config import *
from projectile import Shoot1

class Nitro(pg.sprite.Sprite):
    def load_sprites():
        sprites = LOAD_SPRITES('sprites/chars/nitro')
        return sprites

    def __init__(self, type='', pos=(0, 0)):
        super().__init__()
        self.type = type
        self.sprites = Nitro.load_sprites()
        self.state = 'walk'
        self.last_state = 'walk'
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

        # EQUIPS;
        self.shoots = pg.sprite.Group()
        self.delay = 0
        self.shoot_rate = 8

        # ANIMATION;
        self.image = self.sprites[self.state][self.index]
        self.rect = self.image.get_rect(topleft=(pos))
        self.face_right = True

    def input(self):
        keys = pg.key.get_pressed()

        # SOLO STATES (States que impedem a mudança para outro state enquanto eles não acabam);
        if self.state == 'saber_down':
            self.reset_speed()
            return

        #  JUMP;
        if keys[pg.K_DOWN]:  
            self.gravity = -16
        
        #  SHOOTING;
        if keys[pg.K_LEFT]:
            if self.delay >= self.shoot_rate:
                create_shoot = Shoot1(self,
                                    self.sprites['shoot1'][0],
                                    (self.rect.center[0] + 56, self.rect.center[1] - 24)  # Coordenadas da tela para que seja blitado onde está a ponta da arma;
                                    if self.face_right 
                                    else (self.rect.center[0] - 72, self.rect.center[1] - 24),  # Reajustando a posição caso o player esteja virado para a esquerda;
                                    True if self.face_right else False)  # 'True' para o projetil seguir infinito para frente, 'False' para trás;
                self.shoots.add(create_shoot)
                self.delay = 0
            else:
                self.delay += 1
            print(len(self.shoots))
            
        # MOVIMENTO DE TRÁS E FRENTE;
        if keys[pg.K_a]:  # MOVE LEFT;
            self.movement.x -= 1
            self.face_right = False
        elif keys[pg.K_d]:  # MOVE RIGHT;
            self.movement.x += 1
            self.face_right = True
        if self.movement.x != 0 or self.movement.y != 0:
            self.state = 'walk'
        
        # ATAQUE DE SABRE;
        if keys[pg.K_RIGHT]:
            if self.on_ground:
                self.state = 'saber_down'
            else:
                self.reset_speed()
        else:
            self.reset_speed()
        
        if self.movement.x == 0 and self.on_ground:
            self.stand = True
        else:
            self.stand = False
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
        keys = pg.key.get_pressed()

        if self.state != self.last_state:  # RESETANDO O INDEX CASO MUDE DE STATE;
            self.index = 0

        if keys[pg.K_SPACE]:  # CONTROLANDO O INDEX MANUALMENTE;
            if self.index >= len(self.sprites[self.state]) - 1:
                self.index = 0
            else:
                self.index += 0.1

        if self.state == 'walk':
            if self.movement.x != 0 or self.movement.y != 0:
                if self.index >= len(self.sprites[self.state]) - 1:
                    self.index = 0
                else:
                    self.index += 0.3

        if self.state == 'saber_down':
            if self.index > len(self.sprites[self.state]) - 1:
                self.index = 0
                self.state = 'walk'
            else:
                pass
        
        self.last_state = self.state
    
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
