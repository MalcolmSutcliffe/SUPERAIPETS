import pygame
import os
from SAP_Data import *


class Pet:
    def __init__(self, hp, atk, lvl, status):

        self.base_attack = hp
        self.base_health = atk

        self.level = 1

        self.is_fainted = False

        self.status = status

        self.ability = None

        # self.team = team
        # self.shop = shop
        # self.battleground = battleground
        self.battleground_team = None
        self.battleground_enemy_team = None

        self.temp_attack = 0
        self.temp_health = 0
        self.attack = self.base_attack
        self.health = self.base_health
        self.experience = 0

        try:
            self.rightSprite = pygame.transform.scale(
                pygame.image.load(os.path.join('images/pet_images', self.name_tag + ".png")).convert_alpha(),
                (128, 128))
        except FileNotFoundError:
            self.rightSprite = default_texture
            print("image for '" + input_name + "' not found")
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

    def execute_ability(self):
        # implement ability function
        pass
