import pygame as pg
from level import Level
from config import *


class Game:
    def __init__(self, main, map):
        self.main = main
        self.map = map

        self.level = Level(self.main, self, self.map)

        self.set_debug = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.on = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.main.on = False
                if event.key == pg.K_m:
                    self.main.playing = True
                    self.main.game_playing = False
                if event.key == pg.K_p:
                    if self.set_debug:
                        self.set_debug = False
                    else:
                        self.set_debug = True
    
    def run(self):
        self.check_events()
        self.main.screen.fill('black')
        self.level.run()

        debug(self.main.screen, 
                  'Manaspace.ttf',
                  32,
                  False,
                  '',
                  f'{self.main.fps.get_fps():.0f}',
                  False,
                  pos=(self.main.width - 56, self.main.height - (self.main.height - 32)))
        
        self.main.display.blit(self.main.screen, (0, 0))
