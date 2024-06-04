import pygame as pg
from pygame.image import load

WIDTH = 1024
HEIGHT = 768

def debug(screen, 
          font_path='Manaspace.ttf',
          font_size=0,
          condition=False,
          pre_info='', 
          info='', 
          color=(0, 0, 0), 
          pos=(0, 0)):
    def_font = pg.font.Font(font_path, font_size)
    if condition:
        text = def_font.render(f'{pre_info}: {info}', True, color)
    else:
        text = def_font.render(f'{info}', True, color)
    screen.blit(text, pos)
