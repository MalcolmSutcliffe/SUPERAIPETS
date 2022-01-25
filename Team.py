import copy
import pygame
import json
from Pet import Pet
from SAP_Data import *
from Fonts import *
from AbilityManager import *

class Team:

    def __init__(self,input_name,plural):

        self.pets = [None] * 5  # Type : Pets
        self.lives = 10
        self.wins = 0
        self.turn = DATA.get("turns").get("turn-1")
        self.battleground = None
        self.name = input_name
        if plural:
            self.name_render = mc75.render(self.name+" Win!", False, (255, 255, 255))
        else:
            self.name_render = mc75.render(self.name+" Wins!", False, (255, 255, 255))
        self.name_render_rect = self.name_render.get_rect(center=(SCREEN_WIDTH/2, 200))
        

    def add_pet(self, new_pet, pos):
        if self.pets[pos] is None:
            self.pets[pos] = new_pet
            return 1
        new_pet.set_team(self)
        return 0

    def summon_pet(self, index, summon_tag, summon_attack=0, summon_health=0, level=1, status=None):

        summon_animal = Pet(summon_tag)
        summon_animal.generate_ability()

        if self.battleground is not None:
            teams = [self.battleground.get_team1(), self.battleground.get_team2()]
            summon_animal.set_battleground_team(self)
            teams.remove(self)
            summon_animal.set_battleground_enemy_team(teams[0])
            summon_animal.set_battleground(self.battleground)
        else:
            summon_animal.set_team(self)

        summon_animal.set_base_attack(summon_attack)
        summon_animal.set_base_health(summon_health)
        summon_animal.set_status(status)
        summon_animal.set_level(level)

        self.remove_fainted()
        self.battleground.display()

        if self.has_space():
            has_summoned = False
            self.battleground.display()
            while not has_summoned:
                x = self.pets[index]
                if x is None:
                    self.pets[index] = summon_animal
                    send_triggers(TRIGGER.Summoned, summon_animal, self.battleground)
                    if debug_mode():
                        print(str(summon_animal) + " was summoned with status: " + str(status))
                    has_summoned = True
                else:
                    self.advance_team_from(index)
                    x = self.pets[index]
                    if x is None:
                        self.pets[index] = summon_animal
                        send_triggers(TRIGGER.Summoned, summon_animal, self.battleground)
                        if debug_mode():
                            print(str(summon_animal) + " was summoned with status: " + str(status))
                        has_summoned = True
                    else:
                        self.retreat_team()
        else:
            return

    def sell_pet(self, pos):
        if self.pets[pos] is None:
            return 0
        self.pets[pos] = None
        return 1

    def has_units(self):
        team_has_units = False
        for x in self.pets:
            if x is not None:
                team_has_units = True
                break
        return team_has_units

    def has_space(self):
        team_has_space = False
        for x in self.pets:
            if x is None:
                team_has_space = True
                break
        return team_has_space

    def advance_team(self):
        for j in range(4):
            if self.pets[4 - j] is None:
                self.pets[4 - j] = self.pets[3 - j]
                self.pets[3 - j] = None

    def advance_team_from(self, index):
        for j in range(4-index):
            if self.pets[4-j] is None:
                self.pets[4-j] = self.pets[3-j]
                self.pets[3-j] = None

    def retreat_team(self):
        for j in range(4):
            if self.pets[j] is None:
                self.pets[j] = self.pets[j+1]
                self.pets[j+1] = None

    def remove_fainted(self):
        for (i, x) in enumerate(self.pets):
            if x is not None:
                if x.get_is_fainted():
                    self.pets[i] = None

    # def combine_pet(self, new_pet, pos):
    #     if self.pets[pos] is None:
    #         return -1
    #     elif not (self.pets[pos].name_tag == new_pet.name_tag):
    #         return 0
    #     else:
    #         new_attack = max(new_pet.get_base_attack, self.pets[pos].get_base_attack) + 1
    #         new_health = max(new_pet.get_base_health, self.pets[pos].get_base_health) + 1
    #         self.pets[pos].set_base_attack(new_attack)
    #         self.pets[pos].set_base_health(new_health)
    #         self.pets[pos].gain_exp(1)

    def get_pets(self):
        return self.pets

    def get_name_render(self):
        return self.name_render

    def get_name_render_rect(self):
        return self.name_render_rect
    
    def set_battleground(self, bg):
        self.battleground = bg

    def set_name(self, nameString):
        self.name = nameString
        self.name_render = mc32.render(self.name+" Wins!", False, (255, 255, 255))
        self.name_render_rect = self.name_render.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))


    # def __str__(self):
    #     team_string = []
    #     for pet in self.pets:
    #         team_string.append(pet.get_name_tag())
    #     return str(team_string)
