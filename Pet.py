import pygame
import os

class Pet:

    default_texture = pygame.image.load(os.path.join('images','none.png'))
    
    def __init__(self, name="", base_attack=0, base_health=0, temp_attack=0, temp_health=0, exp=0, item=None, texture=default_texture):
        self.name = name
        self.base_attack = base_attack
        self.base_health = base_health
        self.temp_attack = temp_attack
        self.temp_health = temp_health
        self.attack = base_attack + temp_attack
        self.health = base_health + temp_health
        self.experience = exp
        if self.attack > 50:
            attack = 50
        if self.health > 50:
            health = 50
        self.item = item
        self.rightSprite = texture
        self.leftSprite = pygame.transform.flip(texture, True, False)

    def perform_ability(self):
        return self.item
        # ability goes here

    def get_dmg(self):

        dmg = self.attack

        # if self.item is MEAT_BONE:
        #     dmg += 5
        #
        # if self.item is STEAK:
        #     dmg += 20
        #     self.item.set_active(0)

        return dmg

    def take_damage(self, dmg):

        # if self.item is GARLIC_ARMOR:
        #     if dmg <= 3:
        #         dmg = 1
        #     else:
        #         dmg -= 2
        #
        # if self.item is MELON_ARMOR:
        #     dmg -= 20
        #     self.item.set_active(0)

        if dmg < 0:
            dmg = 0

        self.health -= dmg/2

        if self.health <= 0:
            self.die()

    def die(self):
        return self.health
        # idk, probably better to do in battle

    def gain_stats(self, stats, stat_type=0):  # (0 = permanent stats, #1 = temp stat)
        if stat_type == 0:
            self.base_attack += stats[0]
            self.base_health += stats[1]
        if stat_type == 1:
            self.temp_attack += stats[0]
            self.temp_health += stats[1]

    def gain_exp(self, exp):
        self.experience += exp

    # getters and setters
    def get_attack(self):
        attack = self.base_attack + self.temp_attack
        return self.attack

    def get_health(self):
        health = self.base_health + self.temp_health
        return self.health

    def get_base_attack(self):
        return self.base_attack

    def get_base_health(self):
        return self.base_health

    def get_temp_attack(self):
        return self.temp_attack

    def get_temp_health(self):
        return self.temp_attack

    def get_total_attack(self):
        return self.base_attack + self.temp_attack

    def set_base_attack(self, ba):
        self.base_attack = ba

    def set_base_health(self, bh):
        self.base_health = bh

    def set_temp_attack(self, ta):
        self.temp_attack = ta

    def set_temp_health(self, th):
        self.temp_health = th
