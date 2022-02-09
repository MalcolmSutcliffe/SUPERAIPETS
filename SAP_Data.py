import json
import os
import pygame
import math
from enum import Enum

DEFAULT_ABILITY = {
    "description": "",
    "trigger": "NA",
    "triggeredBy": {
        "kind": "NA"
    },
    "effect": {
        "kind": "NA"
    }
}


class STATUS(Enum):
    WEAK = 1
    COCONUT_SHIELD = 2
    HONEY_BEE = 3
    BONE_ATTACK = 4
    GARLIC_ARMOR = 5
    SPLASH_ATTACK = 6
    MELON_ARMOR = 7
    EXTRA_LIFE = 8
    STEAK_ATTACK = 9
    POISON_ATTACK = 10


class EFFECT_TYPE(Enum):
    AllOf = 1  # implemented
    ApplyStatus = 2  # implemented
    DealDamage = 3  # implemented
    FoodMultiplier = 4  #
    GainExperience = 5  #
    GainGold = 6  #
    ModifyStats = 7  # implemented
    ModifyStatsNotInBattle = 8  #
    OneOf = 9  # implemented
    ReduceHealth = 10  # implemented
    RefillShops = 11  #
    RepeatAbility = 12  # implemented
    SummonPet = 13  # implemented
    SummonRandomPet = 14  # implemented
    Swallow = 15  # implemented
    TransferAbility = 16  #
    TransferStats = 17  # implemented
    NA = 18  # implemented
    Evolve = 19  # implemented


class TARGET(Enum):
    AdjacentAnimals = 1  # implemented
    All = 2  # implemented
    DifferentTierAnimals = 3  # implemented
    EachFriend = 4  # implemented
    EachShopAnimal = 5  # implemented
    FirstEnemy = 6  # implemented
    FriendAhead = 7  # implemented
    FriendBehind = 8  # implemented
    HighestHealthEnemy = 9  # implemented
    LastEnemy = 10  # implemented
    LeftMostFriend = 11  # implemented
    Level2And3Friends = 12  # implemented
    LowestHealthEnemy = 13  # implemented
    RandomEnemy = 14  # implemented
    RandomFriend = 15  # implemented
    RightMostFriend = 16  # implemented
    Self = 17  # implemented
    StrongestFriend = 18  # implemented
    TriggeringEntity = 19  # implemented
    EachEnemy = 20


f = open("data/pet_data.json")
PET_DATA = json.load(f)
f.close()

f = open("data/food_data.json")
FOOD_DATA = json.load(f)
f.close()

f = open("data/status_data.json")
STATUS_DATA = json.load(f)
f.close()

f = open("data/turn_data.json")
TURN_DATA = json.load(f)
f.close()

print(FOOD_DATA)
print(PET_DATA)

default_texture = pygame.image.load(os.path.join('images/pet_images', 'none.png'))

# delay, in seconds
GAME_SPEED = 0.25

SCREEN_WIDTH = 1280

SCREEN_HEIGHT = 720

DEBUG_MODE = False

SFX_ON = True

PACK = "StandardPack"  # can be StandardPack or ExpansionPack1

ANIMAL_TIERS = [[], [], [], [], [], []]

FOOD_TIERS = [[], [], [], [], [], []]

for name in PET_DATA:
    for i in range(6):
        if PET_DATA.get(name).get("tier") == i + 1 and PACK in PET_DATA.get(name).get("packs"):
            ANIMAL_TIERS[i].append(name)
            continue

for name in FOOD_DATA:
    for i in range(6):
        if FOOD_DATA.get(name).get("tier") == i + 1: # and PACK in PET_DATA.get(name).get("packs"):
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
        GAME_SPEED = 1 / (2 ** (speed - 1))


def get_game_speed():
    global GAME_SPEED
    return GAME_SPEED


def sfx_on():
    return SFX_ON
