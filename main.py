import pygame as pg
from game import Game
from editor import Editor
from level import Level
from config import *
from pygame.image import load
from maps import map01

pg.init()

display = pg.display.set_mode((1024, 768))
pg.display.set_caption('RE: Metal Warriors V2.0')

class Main:
    def __init__(self, display):
        self.display = display

        self.tile_set = 128
        self.width = 1024
        self.height = 768
        self.main_screen = pg.Surface((self.width, self.height))
        self.main_screen.fill('black')
        self.fps = pg.time.Clock()

        # GAME INSTANCES;
        self.game = Game(self)
        self.editor = Editor(self)
        self.level = Level(self, self.game, map01)

        # GAME TRANSITIONS;
        self.on = True
        self.main_playing = False
        self.game_playing = True
        self.editor_playing = False
    
        # MAIN MENU
        self.nitro_menu_path = 'sprites/chars/nitro/walk/'
        self.nitro_loop = {'sprites': [self.nitro_menu_path + '00.png',
                                       self.nitro_menu_path + '01.png', 
                                       self.nitro_menu_path + '02.png',
                                       self.nitro_menu_path + '03.png',
                                       self.nitro_menu_path + '04.png',
                                       self.nitro_menu_path + '05.png',
                                       self.nitro_menu_path + '06.png',
                                       self.nitro_menu_path + '07.png'], 
                           'index': 0}
    
    def main_menu_loop(self):
        if self.nitro_loop['index'] >= 7:
            self.nitro_loop['index'] = 0
        else:
            self.nitro_loop['index'] += 0.2

    def check_events(self):
        for event in pg.event.get():
            # SHUTTING THE GAME;
            if event.type == pg.QUIT:
                self.on = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.on = False

                # SWITCH TO GAME;
                if event.key == pg.K_g:
                    self.game_playing = True
                    self.main_playing = False
                # SWITCH TO EDITOR;
                if event.key == pg.K_e:
                    self.editor_playing = True
                    self.main_playing = False

    def run(self):
        while self.on:
            display.fill('black')
            if self.main_playing:
                self.main_screen.fill('black')
                self.check_events()
                self.main_menu_loop()
                self.main_screen.blit(self.nitro_loop['sprites'][int(self.nitro_loop['index'])], (self.width / 2 - 64, self.height / 4))
                display.blit(self.main_screen, ((0, 0)))

            if self.game_playing:
                self.game.screen.fill('black')
                self.game.check_events()
                self.level.run()
                display.blit(self.game.screen, (0, 0))
            
            if self.editor_playing:
                self.editor.screen.fill('green')
                self.editor.check_events()
                display.blit(self.editor.screen, (0, 0))
            
            debug(display, 'Manaspace.ttf', 32, False, '', f'{self.fps.get_fps():.0f}', (255, 255, 255), (984, 0))
            pg.display.update()
            self.fps.tick(60)


main = Main(display)
main.run()
