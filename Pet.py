import copy

import pygame
import random

from PetAbility import PetAbility
from AbilityManager import *
from SAP_Data import *
import os

pygame.mixer.init()
fuck = pygame.mixer.Sound("audio/sfx/fuck.wav")


def generate_random_pet():
    new_pet = Pet(random.sample(random.sample(AVAILABLE_ANIMALS, 1)[0], 1)[0][4:])
    return new_pet


class Pet:

    def __init__(self, input_name="", status=None, level=1, ability_data=DEFAULT_ABILITY, team=None, location=None):

        # create pet with default stats.

        self.name = input_name
        self.base_attack = 1
        self.base_health = 1
        self.temp_attack = 0
        self.temp_health = 0
        self.experience = 0
        self.level = level
        self.tier = 1
        self.packs = ["StandardPack"]

        self.attack = self.base_attack
        self.health = self.base_health

        self.is_fainted = False
        self.status = status
        self.ability_data = ability_data

        self.team = team

        self.location = location

        if team is not None:
            self.location = team.get_location()

        self.name_tag = "pet-" + input_name
        self.pet_data = PET_DATA.get("bee")

        self.rightSprite = pygame.transform.scale(default_texture, (128, 128))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

        # try opening file, if it doesn't exist, returns, pet will be a bee.
        try:
            self.pet_data = PET_DATA.get(self.name_tag)
        except AttributeError:
            print("Error: the pet tag '" + self.name_tag + "' does not exist!")
            return

        # try applying the unique pet stats
        try:
            self.base_attack = self.pet_data.get("baseAttack")
            self.base_health = self.pet_data.get("baseHealth")
            self.packs = self.pet_data.get("packs")
            self.tier = self.pet_data.get("tier")
            self.ability_data = self.pet_data.get("level" + str(self.level) + "Ability")
        except AttributeError:
            pass

        # update attack and health
        self.attack = self.base_attack
        self.health = self.base_health

        # set ability
        self.ability = PetAbility(self, self.ability_data)

        # Note this will be replaced, when a scorpion is summoned it will have the status passed to it
        # if self.name == "scorpion":
        #     self.status = STATUS.POISON_ATTACK

        try:
            self.rightSprite = pygame.transform.scale(
                pygame.image.load(os.path.join('images/pet_images', self.name_tag + ".png")).convert_alpha(),
                (128, 128))
        except FileNotFoundError:
            print("image for '" + input_name + "' not found")

        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

    def receive_trigger(self, trigger, triggering_entity):
        if self.ability is None:
            return
        if trigger[0] == self.ability.get_trigger() and trigger[1] == self.ability.get_triggered_by():
            self.ability.triggering_entity = triggering_entity
            send_triggers(TRIGGER.CastsAbility, self, self.get_location())
            self.team.get_location().AM.add_to_queue(self.ability)

    def get_dmg(self):

        dmg = self.attack

        if self.status == STATUS.STEAK_ATTACK:
            dmg += 20
            self.status = None

        if self.status == STATUS.BONE_ATTACK:
            dmg += 5

        return dmg

    def attack_enemy(self, victim):

        if self.status == STATUS.SPLASH_ATTACK:
            team = victim.get_team().get_pets()
            index = victim.get_index()
            for j in range(1, index):
                if index - j >= 0 and team[index - j] is not None:
                    team[index - j].take_damage(self, self.get_dmg())
                    break

        victim.take_damage(self, self.get_dmg())

    def take_damage(self, attacker, dmg):

        send_hurt = True

        if self.status == STATUS.WEAK:
            dmg += 3

        if self.status == STATUS.GARLIC_ARMOR:
            dmg -= 2
            if dmg < 2:
                dmg = 1

        if self.status == STATUS.MELON_ARMOR:
            dmg -= 20
            if dmg < 0:
                dmg = 0
                send_hurt = False
            self.status = None

        if self.status == STATUS.COCONUT_SHIELD:
            dmg = 0
            self.status = None
            send_hurt = False

        if get_debug_mode():
            print(str(self) + " took " + str(dmg) + " dmg ")

        self.health = self.health - dmg

        if dmg >= 1 and attacker.get_status() == STATUS.POISON_ATTACK:
            self.health = 0

        if self.health <= 0 and not self.is_fainted:
            self.faint()
            send_triggers(TRIGGER.KnockOut, attacker, self.get_location())

        if send_hurt:
            send_triggers(TRIGGER.Hurt, self, self.get_location())

    def faint(self):

        if sfx_on():
            pygame.mixer.Sound.play(fuck)
        if get_debug_mode():
            print(self.name + " has fainted!")

        self.is_fainted = True

        send_triggers(TRIGGER.Faint, self, self.get_location())

        team = self.get_team()

        if self.status == STATUS.HONEY_BEE:
            team.summon_pet(self.get_index(), "bee", 1, 1, None)
            pass

        if self.status == STATUS.EXTRA_LIFE:
            team.summon_pet(self.get_index(), self.name, 1, 1, None)
            pass

    def gain_stats(self, stats, stat_type=0):  # (0 = permanent stats, #1 = temp stat)
        if stat_type == 0:
            self.base_attack += stats[0]
            self.base_health += stats[1]
        if stat_type == 1:
            self.temp_attack += stats[0]
            self.temp_health += stats[1]
        self.attack += stats[0]
        self.health += stats[1]
        if get_debug_mode():
            print(str(self) + " gained " + str(stats[0]) + " attack and " + str(stats[1]) + " health.")

    def gain_exp(self, exp):
        self.experience += exp
        if 2 <= self.experience < 6:
            self.level = 2
        elif 6 <= self.experience:
            self.level = 3

    def generate_ability(self):
        self.ability = PetAbility(self)
        pass

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

    def get_team(self):
        return self.team

    def get_enemy_team(self):
        return self.team.get_enemy_team()

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

    def get_location(self):
        return self.get_team().get_location()

    def get_index(self):
        return self.get_team().get_pets().index(self)

    def set_team(self, team):
        self.team = team

    def set_base_attack(self, ba):
        self.base_attack = ba
        self.attack = self.base_attack + self.temp_attack

    def set_attack(self, atk):
        self.attack = atk

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
        self.name_tag = pet_to_copy.name_tag
        self.name = pet_to_copy.name
        pet_data = PET_DATA.get("bee")
        try:
            pet_data = PET_DATA.get(self.name_tag)
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

    def deep_copy(self):
        new_pet = copy.copy(self)
        new_pet.ability = self.get_ability().deep_copy()
        return new_pet

    def __str__(self):
        return self.name
