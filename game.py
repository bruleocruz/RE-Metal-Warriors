import pygame as pg
from level import Level


class Game:
    def __init__(self, main, map):
        self.main = main
        self.map = map

        self.level = Level(self.main, self, self.map)

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
    
    def run(self):
        self.check_events()
        self.main.screen.fill('black')
        self.level.run()

        self.main.display.blit(self.main.screen, (0, 0))