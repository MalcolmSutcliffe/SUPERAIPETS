import json
import os
import pygame
import math

f = open("SAPinfo.json")
DATA = json.load(f)
f.close()

default_texture = pygame.image.load(os.path.join('images/pet-images', 'none.png'))

#delay, in seconds
GAME_SPEED = 0.25

SCREEN_WIDTH = 1280

SCREEN_HEIGHT = 720

DEBUG_MODE = False

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


def set_debug_mode(boolean):
    global DEBUG_MODE
    DEBUG_MODE = boolean

def get_debug_mode():
    return DEBUG_MODE

def change_game_speed(speed):
    global GAME_SPEED
    if speed == 0:
        GAME_SPEED = 0
    else:
        GAME_SPEED = 1/(2**(speed-1))

def get_game_speed():
    global GAME_SPEED
    return GAME_SPEED

