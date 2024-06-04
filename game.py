import pygame as pg


class Game:
    def __init__(self, main):
        self.main = main
        self.screen = pg.Surface(((self.main.tile_set * 64), (self.main.tile_set * 64)))

    def check_events(self):
        for event in pg.event.get():
            # SHUTTING THE GAME;
            if event.type == pg.QUIT:
                self.main.on = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.main.on = False

                # SWITCH TO MAIN;
                if event.key == pg.K_m:
                    self.main.main_playing = True
                    self.main.game_playing = False
                # SWITCH TO EDITOR;
                if event.key == pg.K_e:
                    self.main.editor_playing = True
                    self.main.game_playing = False
