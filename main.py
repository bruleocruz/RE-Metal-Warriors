import pygame as pg
from game import Game
from entity import Nitro
from config import *
from maps import *
import sys


pg.init()


class Main:
    def __init__(self, tile_set):
        self.tile_set = tile_set
        self.width = tile_set * 8
        self.height = tile_set * 6
        self.display = pg.display.set_mode((self.width, self.height))
        self.fps = pg.time.Clock()

        self.screen = pg.Surface((self.width, self.height))

        # INSTANCES;
        self.game = Game(self, map01)

        self.on = True

        self.playing = False
        self.game_playing = True
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.on = False
            if event.type == pg.KEaaaYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.on = False
                if event.key == pg.K_g:
                    self.game_playing = True
                    self.playing = False
        
    def run(self):
        while self.on:
            if self.playing:
                self.check_events()
                self.screen.fill('green')
                self.display.blit(self.screen, (0, 0))
                   
            if self.game_playing:
                self.game.run()

            pg.display.update()
            self.fps.tick(60)
            

main = Main(128)
main.run()
