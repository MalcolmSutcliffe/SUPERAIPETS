import pygame
import os
import json
from PetAbility import PetAbility
import AbilityManager
from AbilityManager import *
from SAP_Data import DATA

default_texture = pygame.image.load(os.path.join('images/pet-images', 'none.png'))


class Pet:

    def __init__(self, name_tag="", team=None, battleground=None):

        self.base_attack = 1
        self.base_health = 1

        self.level = 1

        self.team = team
        self.battleground = battleground
        self.battleground_team = None
        self.battleground_enemy_team = None

        self.name_tag = "pet-" + name_tag
        pet_data = DATA.get("pets").get("bee")

        try:
            pet_data = DATA.get("pets").get(self.name_tag)
        except AttributeError:
            print("Error: the pet tag '" + self.name_tag + "' does not exist!")

        self.base_attack = pet_data.get("baseAttack")
        self.base_health = pet_data.get("baseHealth")
        self.packs = pet_data.get("packs")
        self.ability = PetAbility(self)
        self.tier = pet_data.get("tier")
        self.temp_attack = 0
        self.temp_health = 0
        self.attack = self.base_attack
        self.health = self.base_health
        self.experience = 0
        self.status = None
        try:
            self.rightSprite = pygame.transform.scale(
                pygame.image.load(os.path.join('images/pet-images', self.name_tag + ".png")), (128, 128))
        except FileNotFoundError:
            self.rightSprite = default_texture
            print("image for '" + name_tag + "' not found")
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

    # def perform_ability(self):
    #     print(self.name_tag + " performed his ability!")
    #     # ability goes here

    def receive_trigger(self, trigger):
        if trigger[0] == self.ability.get_trigger() and trigger[1] == self.ability.get_triggered_by():
            self.battleground.AM.add_to_queue(self.ability)
            # print(self.name_tag + " received his ability!")

    def get_dmg(self):

        dmg = self.attack

        # if self.item is MEAT_BONE:
        #     dmg += 5
        #
        # if self.item is STEAK:
        #     dmg += 20
        #     self.item.set_active(0)

        return dmg

    def take_damage(self, attacker):

        # if self.item is GARLIC_ARMOR:
        #     if dmg <= 3:
        #         dmg = 1
        #     else:
        #         dmg -= 2
        #
        # if self.item is MELON_ARMOR:
        #     dmg -= 20
        #     self.item.set_active(0)

        # if dmg < 0:
        #     dmg = 0

        dmg = attacker.get_attack()

        self.health = self.health - dmg

        send_triggers_battle(TRIGGER.Hurt, self, self.battleground)

        # print(self.battleground_team)

        if self.health <= 0:
            self.faint()

    def faint(self):
        send_triggers_battle(TRIGGER.Faint, self, self.battleground)
        self.battleground_team[self.battleground_team.index(self)] = None
        # self.battleground_team = None
        # self.battleground_enemy_team = None
        # self.battleground = None
        print("animal '" + self.name_tag + "' has fainted!")
        # self.battleground = None

    def gain_stats(self, stats, stat_type=0):  # (0 = permanent stats, #1 = temp stat)
        if stat_type == 0:
            self.base_attack += stats[0]
            self.base_health += stats[1]
        if stat_type == 1:
            self.temp_attack += stats[0]
            self.temp_health += stats[1]

    def gain_exp(self, exp):
        self.experience += exp
        if 2 <= self.experience < 6:
            self.level = 2
        elif 6 <= self.experience:
            self.level = 3

    def generate_ability(self):
        self.ability = PetAbility(self)

    # getters and setters
    def get_name_tag(self):
        return self.name_tag

    def get_attack(self):
        return self.attack

    def get_health(self):
        return self.health

    def get_battleground(self):
        return self.battleground

    def get_team(self):
        return self.team

    def get_battleground_team(self):
        return self.battleground_team

    def get_battleground_enemy_team(self):
        return self.battleground_enemy_team

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

    def set_battleground(self, bg):
        self.battleground = bg

    def set_battleground_team(self, bg_team):
        self.battleground_team = bg_team

    def set_battleground_enemy_team(self, bg_en_team):
        self.battleground_enemy_team = bg_en_team

    def set_base_attack(self, ba):
        self.base_attack = ba

    def set_base_health(self, bh):
        self.base_health = bh

    def set_temp_attack(self, ta):
        self.temp_attack = ta

    def set_temp_health(self, th):
        self.temp_health = th

    def __str__(self):
        return self.name_tag + " | HP: " + str(self.health) + " | Attack: " + str(self.attack)