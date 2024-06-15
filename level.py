import pygame as pg
from tiles import Tile
from pygame.image import load
from entity import Nitro
from config import *


class Level:
    def __init__(self, main, game, map):
        self.main = main
        self.game = game
        self.map = map

        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

        self.set_level(map)

    def set_level(self, map):
        for y, y_index in enumerate(map):
            for x, x_index in enumerate(y_index):
                x_pos = x * self.main.tile_set
                y_pos = y * self.main.tile_set

                if x_index == 'b':
                    create_tile = Tile(load('sprites/wall000.png').convert_alpha(), (x_pos, y_pos), 'collide', 0)
                    self.tiles.add(create_tile)

                # PLAYER;
                if x_index == 'c':
                    create_player = Nitro('', (x_pos, y_pos))
                    self.player.add(create_player)
    
    def camera_limit(self, player):
            width = self.main.width / 2
            height = self.main.height / 2
            x_limit = [False, False]

            if player.rect.x < width - 200:
                player.rect.x = width - 200
                x_limit[0] = True
            if player.rect.x > width + 200 - 128:
                player.rect.x = width + 200 - 128
                x_limit[1] = True
            
            return x_limit        
    
    def check_collision(self, player, tiles):
        list = []

        for tile in tiles:
            if player.rect.colliderect(tile):
                list.append(tile)
        
        return list

    def apply_x_collision(self, player, tiles):
        for tile in tiles:
            if player.movement.x < 0:
                player.rect.left = tile.rect.right
                player.movement.x = 0
                player.on_left = True
            if player.movement.x > 0:
                player.rect.right = tile.rect.left
                player.movement.x = 0
                player.on_right = True
        
        if player.on_left and player.movement.x != 0:
            player.on_left = False
        if player.on_right and player.movement.x != 0:
            player.on_right = False
    
    def apply_y_collision(self, player, tiles):
        for tile in tiles:
            if player.movement.y < 0:
                player.rect.top = tile.rect.bottom
                player.movement.y = 0
                player.gravity = 0
                player.on_ceiling = True
            if player.movement.y > 0:
                player.rect.bottom = tile.rect.top
                player.movement.y = 0
                player.gravity = 0
                player.on_ground = True
            
        if player.on_ceiling and player.movement.y != 0:
            player.on_ceiling = False
        if player.on_ground and player.movement.y != 0:
            player.on_ground = False
    
    def center_player(self, player, tiles, shoots):
        x_value = 0
        y_value = 0
        distance = 16  # Quanto maior essa variável, menor será o valor que irá puxar o player para o centro da tela, 
                       # resultando em uma distancia maior de locomoção para longe do centro;

        if player.rect.center[0] < self.main.width / 2:
            x_value = int((self.main.width / 2 - player.rect.center[0]) / distance)
            player.rect.x += x_value
        if player.rect.center[0] > self.main.width / 2:
            x_value = int((self.main.width / 2 - player.rect.center[0]) / distance)
            player.rect.x += x_value
        if player.rect.center[1] < self.main.height / 2:
            y_value = int((self.main.height / 2 - player.rect.center[1]) / distance)
            player.rect.y += y_value
        if player.rect.center[1] > self.main.height / 2:
            y_value = int((self.main.height / 2 - player.rect.center[1]) / distance)
            player.rect.y += y_value

        for tile in tiles:  # Movimentando todos os tiles junto com o player, para que não tenha problemas de colisão;
            if player.rect.x < self.main.width / 2:
                tile.rect.x += x_value
            if player.rect.x > self.main.width / 2:
                tile.rect.x += x_value
            if player.rect.y < self.main.height / 2:
                tile.rect.y += y_value
            if player.rect.y > self.main.height / 2:
                tile.rect.y += y_value
        
        for shoot in shoots:  # Mesmo processo de cima, porém agora com os projeteis (provavelmente terá que fazer isso com muitos elementos...);
            shoot.update()

            if player.rect.x < self.main.width / 2:
                shoot.rect.x += x_value
            if player.rect.x > self.main.width / 2:
                shoot.rect.x += x_value
            if player.rect.y < self.main.height / 2:
                shoot.rect.y += y_value
            if player.rect.y > self.main.height / 2:
                shoot.rect.y += y_value
                
            if shoot.rect.x > self.main.width or shoot.rect.x < 0:
                shoot.kill()  # Método da classe 'sprite.Group' que deleta o sprite caso algo aconteça;
            if shoot.rect.y > self.main.height or shoot.rect.y < 0:
                shoot.kill()
    
    def move(self):
        player = self.player.sprite
        shoots = player.shoots.sprites()
        tiles = self.tiles.sprites()

        player.update()
        player.apply_gravity()

        # APLICANDO AS COLISÕES E CORRIGINDO A POSIÇÃO DO PLAYER COM OS TILES;
        player.apply_movement_y()
        self.apply_y_collision(player, self.check_collision(player, tiles)) 
        player.apply_movement_x()
        self.apply_x_collision(player, self.check_collision(player, tiles))

        # MOVIMENTANDO OS TILES BASEADO NO MOVIMENTO DO PLAYER NO EIXO X;
        limit = self.camera_limit(player)  # Essa variável retorna uma lista de dois valores boleanos, 
                                           # que são trigados caso o player atinja o limite de distância em referencia ao meio da tela;
        for tile in tiles:
            if limit[0]:
                tile.rect.x += n_p(player.movement.x)
            if limit[1]:
                tile.rect.x += p_n(player.movement.x)
        
        self.center_player(player, tiles, shoots)
    
    def debug(self, player):
        # DEBUG SPACE;
        if self.game.set_debug:
            ############################################ BLOCO 1;
            if self.game.debug_1:
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'Ceiling',
                    player.on_ceiling,
                    True,
                    pos=(0, 0))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'Ground',
                    player.on_ground,
                    True,
                    pos=(0, 16))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'Left',
                    player.on_left,
                    True,
                    pos=(0, 32))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'Right',
                    player.on_right,
                    True,
                    pos=(0, 48))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'Stand',
                    player.stand,
                    True,
                    pos=(0, 64))
            ############################################ BLOCO 2;
            if self.game.debug_2:
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'movement x',
                    player.movement.x,
                    False,
                    pos=(128, 0))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'movement y',
                    player.movement.y,
                    False,
                    pos=(128, 16))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'pos x',
                    player.rect.x,
                    False,
                    pos=(128, 32))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'pos y',
                    player.rect.y,
                    False,
                    pos=(128, 48))
            ############################################ BLOCO 2;
            if self.game.debug_3:
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'State',
                    player.state,
                    False,
                    pos=(256, 0))
                debug(self.main.screen, 
                    'ARIAL.TTF',
                    16,
                    True,
                    'Index',
                    f'{player.index:.0f}',
                    False,
                    pos=(256, 16))

    def run(self):
        self.move()

        self.tiles.draw(self.main.screen)
        self.player.draw(self.main.screen)
        self.player.sprite.shoots.draw(self.main.screen)
        self.debug(self.player.sprite)
    