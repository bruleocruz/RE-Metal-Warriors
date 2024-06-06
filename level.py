import pygame as pg
from tiles import InteractibleTile, NotInteractibleTile
from player import Nitro
from config import debug, n_p, p_n


class Level:
    def __init__(self, main, game, map):
        self.main = main
        self.game = game
        self.map = map

        self.last_x_collide = ()

        # GROUPS;
        self.interactible_tiles = pg.sprite.Group()
        self.notinteractibletiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

        self.set_level()
    
    def set_level(self):
        for y, y_index in enumerate(self.map):
            for x, x_index in enumerate(y_index):
                x_pos = x * self.main.tile_set
                y_pos = y * self.main.tile_set

                if x_index == 'b':
                    create_tile = InteractibleTile(x_pos, y_pos, pg.Surface((128, 128)))
                    self.interactible_tiles.add(create_tile)
                
                # PLAYER;
                if x_index == 'c':
                    create_player = Nitro(x_pos, y_pos)
                    self.player.add(create_player)

    def player_camera_limit(self, player, tiles):
        l_limit = [(self.main.width / 2) - 200, False]
        r_limit = [(self.main.width / 2) + 200, False]
        u_limit = [(self.main.height / 2) - 200, False]
        d_limit = [(self.main.height / 2) + 200, False]

        if player.rect.left <= l_limit[0]:
            player.rect.left = l_limit[0]
            l_limit[1] = True
        elif player.rect.right >= r_limit[0]:
            player.rect.right = r_limit[0]
            r_limit[1] = True
        if player.rect.top <= u_limit[0]:
            player.rect.top = u_limit[0]
            u_limit[1] = True
        elif player.rect.bottom >= d_limit[0]:
            player.rect.bottom = d_limit[0]
            d_limit[1] = True     

        for tile in tiles:
            if l_limit[1]:
                tile.rect.x += n_p(player.axis.x)
            elif r_limit[1]:
                tile.rect.x += p_n(player.axis.x)
            if u_limit[1]:
                tile.rect.y += n_p(player.axis.y)
            elif d_limit[1]:
                tile.rect.y += p_n(player.axis.y)

    def check_collide(self, player, tiles):
        list = []
        for tile in tiles:
            if player.rect.colliderect(tile):
                list.append(tile)
        return list

    def x_collide(self, player, tiles):
        for tile_collide in self.check_collide(player, tiles):
            if player.axis.x < 0:
                player.rect.left = tile_collide.rect.right
                player.on_left = True
                player.axis.x = 0
                self.last_x_collide = player.rect.left
            if player.axis.x > 0:
                player.rect.right = tile_collide.rect.left
                player.on_right = True
                player.axis.x = 0
                self.last_x_collide = player.rect.right

    def y_collide(self, player, tiles):
        for tile_collide in self.check_collide(player, tiles):
            if tiles:
                if player.axis.y > 0:
                    player.rect.bottom = tile_collide.rect.top
                    player.on_ground = True
                    player.axis.y = 0
                elif player.axis.y < 0:
                    player.rect.top = tile_collide.rect.bottom
                    player.on_ceiling = True
                    player.axis.y = 0
    
    def apply_collides(self):
        player = self.player.sprite
        tiles = self.interactible_tiles.sprites()

        # THE PLAYER ACCELERATION AND GRAVITY WILL BE APPLIED HERE;
        player.command_button()
        player.gravity()

        player.apply_gravity()
        self.y_collide(player, tiles)
        player.apply_movement()
        self.x_collide(player, tiles)
        self.player_camera_limit(player, tiles)

        if player.on_left and player.rect.left != self.last_x_collide:
            player.on_left = False
        if player.on_right and player.rect.right != self.last_x_collide:
            player.on_right = False

        if player.on_ground and player.axis.x == 0 and player.axis.y == 0:
            player.stand = True
        else:
            player.stand = False

        if player.on_ceiling and player.axis.y > 0 or player.on_ceiling and player.on_ground:
            player.on_ceiling = False
        if player.on_ground and player.axis.y != 0 or player.on_ground and player.on_ceiling:
            player.on_ground = False

    def player_info(self):
        font = pg.font.Font('ARIAL.ttf', 16)
        player = self.player.sprite

        # GET INFO;
        state = font.render(f'State: {player.state}', True, (255, 255, 255))
        index = font.render(f'Index: {player.index:.0f}', True, (255, 255, 255))
        ceiling = font.render(f'On Ceiling: {player.on_ceiling}', True, (0, 255, 0) if player.on_ceiling else (255, 0, 0))
        ground = font.render(f'On Ground: {player.on_ground}', True, (0, 255, 0) if player.on_ground else (255, 0, 0))
        left = font.render(f'On Left: {player.on_left}', True, (0, 255, 0) if player.on_left else (255, 0, 0))
        right = font.render(f'On Right: {player.on_right}', True, (0, 255, 0) if player.on_right else (255, 0, 0))
        stand = font.render(f'Stand: {player.stand}', True, (0, 255, 0) if player.stand else (255, 0, 0))
        x_pos = font.render(f'Pos X: {player.rect.x}', True, (255, 255, 255))
        y_pos = font.render(f'Pos Y: {player.rect.y}', True, (255, 255, 255))
        axis_x = font.render(f'Speed: {player.axis.x}', True, (255, 255, 255))
        axis_y = font.render(f'Gravity: {player.axis.y}', True, (255, 255, 255))
         
        # BLIT SPACE;
        self.game.screen.blit(state, (0, 0))
        self.game.screen.blit(index, (0, 16))
        self.game.screen.blit(ceiling, (0, 32))
        self.game.screen.blit(ground, (0, 48))
        self.game.screen.blit(left, (0, 64))
        self.game.screen.blit(right, (0, 80))
        self.game.screen.blit(stand, (0, 96))
        self.game.screen.blit(x_pos, (128, 0))
        self.game.screen.blit(y_pos, (128, 16))
        self.game.screen.blit(axis_x, (128, 32))
        self.game.screen.blit(axis_y, (128, 48))        

    def run(self):
        self.interactible_tiles.update()
        self.player.update()

        self.apply_collides()

        self.interactible_tiles.draw(self.game.screen)
        self.player.draw(self.game.screen)

        self.player_info()
