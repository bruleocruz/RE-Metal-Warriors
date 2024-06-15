import pygame as pg
from pygame.image import load
from os import walk, listdir


WIDTH = 1024
HEIGHT = 768
SPRITE_PATH = 'sprites/'

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

def n_p(x):  # CONVERT NEGATIVE TO POSITIVE;
    return int((x * -2) / 2)

def p_n(x):  # CONVERT POSITIVE TO NEGATIVE;
    return int(x - (x * 2))

def LOAD_SPRITES(path):
    sprites = {}

    # Convertendo o nome das pastas para keys de um dicionário e criando uma lista vazia em cima delas;
    for a, b, c in walk(path):
        # ADICIONANDO NOME DAS PASTAS NO DICIONÁRIO;
        for name in b:
            sprites[name] = []
        
    for key, value in sprites.items():
        new_path = path + '/' + key  # Criando um path novo baseado na key(nome da pasta) que o loop se encontra;
        for a, b, c in walk(new_path):
            for file in c:  # A variável 'c' representa o nome dos arquivos separadamente dentro da pasta específica;
                sprites[key].append(load(new_path + '/' + file).convert_alpha())
    
    return sprites
