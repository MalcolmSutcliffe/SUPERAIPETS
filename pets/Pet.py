import pygame
import os
import random
from SAP_Data import *


def generate_random_pet():
    new_pet = Pet(random.sample(random.sample(ANIMAL_TIERS, 1)[0], 1)[0][4:])
    return new_pet


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

    def get_dmg(self):

        dmg = self.attack

        if self.status == STATUS.STEAK_ATTACK:
            dmg += 20
            self.status = None

        if self.status == STATUS.BONE_ATTACK:
            dmg += 5

        return dmg

    # getters and setters
    def get_name(self):
        return self.name

    def get_name_tag(self):
        return self.name_tag

    def get_sprite(self, direction):
        if direction == 0:
            return self.leftSprite
        elif direction == 1:
            return self.rightSprite
        else:
            return default_texture

    def get_attack(self):
        return self.attack

    def get_health(self):
        return self.health

    def get_base_attack(self):
        return self.base_attack

    def get_base_health(self):
        return self.base_health

    def get_temp_attack(self):
        return self.temp_attack

    def get_temp_health(self):
        return self.temp_attack

    def get_level(self):
        return self.level

    def get_tier(self):
        return self.tier

    def get_is_fainted(self):
        return self.is_fainted

    def get_status(self):
        return self.status

    def get_ability(self):
        return self.ability

    def get_index(self):

        team = self.battleground_team
        if team is None:
            team = self.team
        if team is None:
            return -1

        return team.get_pets().index(self)

    def set_team(self, team):
        self.team = team

    def set_battleground(self, bg):
        self.battleground = bg

    def set_battleground_team(self, bg_team):
        self.battleground_team = bg_team

    def set_battleground_enemy_team(self, bg_en_team):
        self.battleground_enemy_team = bg_en_team

    def set_base_attack(self, ba):
        self.base_attack = ba
        self.attack = self.base_attack + self.temp_attack

    def set_attack(self, atck):
        self.attack = atck

    def set_base_health(self, bh):
        self.base_health = bh
        self.health = self.base_health + self.temp_health

    def set_health(self, health):
        self.health = health

    def set_temp_attack(self, ta):
        self.temp_attack = ta

    def set_temp_health(self, th):
        self.temp_health = th

    def set_status(self, status):
        self.status = status

    def set_level(self, lvl):
        self.level = lvl

    def copy_pet(self, pet_to_copy):
        self.base_attack = pet_to_copy.base_attack
        self.base_health = pet_to_copy.base_health
        self.level = pet_to_copy.level
        self.is_fainted = pet_to_copy.is_fainted
        self.status = pet_to_copy.status
        self.ability = pet_to_copy.Ability
        self.team = None
        self.shop = None
        self.battleground = None
        self.battleground_team = None
        self.battleground_enemy_team = None
        self.name_tag = pet_to_copy.name_tag
        self.name = pet_to_copy.name
        pet_data = DATA.get("pets").get("bee")
        try:
            pet_data = DATA.get("pets").get(self.name_tag)
        except AttributeError:
            print("Error: the pet tag '" + self.name_tag + "' does not exist!")
        try:
            self.base_attack = pet_data.get("baseAttack")
            self.base_health = pet_data.get("baseHealth")
            self.packs = pet_data.get("packs")
            self.tier = pet_data.get("tier")
        except AttributeError:
            pass
        self.temp_attack = 0
        self.temp_health = 0
        self.attack = self.base_attack
        self.health = self.base_health
        self.experience = 0
        if self.name == "scorpion":
            self.status = STATUS.POISON_ATTACK
        try:
            self.rightSprite = pygame.transform.scale(
                pygame.image.load(os.path.join('images/pet-images', self.name_tag + ".png")), (128, 128))
        except FileNotFoundError:
            self.rightSprite = default_texture
            print("image for '" + self.name_tag + "' not found")
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

    def __str__(self):
        return self.name
