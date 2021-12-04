import json
import os
import pygame

f = open("SAPinfo.json")
DATA = json.load(f)
f.close()

default_texture = pygame.image.load(os.path.join('images/pet-images', 'none.png'))

GAME_SPEED = 0.5
