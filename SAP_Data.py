import json
import os
import pygame

f = open("SAPinfo.json")
DATA = json.load(f)
f.close()

default_texture = pygame.image.load(os.path.join('images/pet-images', 'none.png'))

GAME_SPEED = 0.5

DEBUG_MODE = 0

ANIMAL_TIERS = [[], [], [], [], [], []]

FOOD_TIERS = [[], [], [], [], [], []]

for name in DATA.get("pets"):
    for i in range(6):
        if DATA.get("pets").get(name).get("tier") == i+1:
            ANIMAL_TIERS[i].append(name)
            continue

for name in DATA.get("foods"):
    for i in range(6):
        if DATA.get("foods").get(name).get("tier") == i+1:
            FOOD_TIERS[i].append(name)
            continue


def toggle_debug():
    global DEBUG_MODE
    if DEBUG_MODE == 0:
        DEBUG_MODE = 1
    else:
        DEBUG_MODE = 0
    print(DEBUG_MODE)

def debug_mode():
    return DEBUG_MODE
