import pygame as pg


class Editor:
    def __init__(self, main):
        self.main = main
        self.screen = pg.Surface((self.main.tile_set * 16, self.main.tile_set * 12))
    
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
                    self.main.editor_playing = False
                # SWITCH TO GAME;
                if event.key == pg.K_g:
                    self.main.game_playing = True
                    self.main.editor_playing = False
