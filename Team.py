import copy

from Pet import Pet


class Team:

    def __init__(self):
        self.pets = [None] * 5  # Type : Pets

    def add_pet(self, new_pet, pos):
        if self.pets[pos] is None:
            self.pets[pos] = new_pet
            return 1
        return 0

    def sell_pet(self, pos):
        if self.pets[pos] is None:
            return 0
        self.pets[pos] = None
        return 1

    def combine_pet(self, new_pet, pos):
        if self.pets[pos] is None:
            return -1
        elif not (self.pets[pos].name_tag == new_pet.name_tag):
            return 0
        else:
            new_attack = max(new_pet.get_base_attack, self.pets[pos].get_base_attack) + 1
            new_health = max(new_pet.get_base_health, self.pets[pos].get_base_health) + 1
            self.pets[pos].set_base_attack(new_attack)
            self.pets[pos].set_base_health(new_health)
            self.pets[pos].gain_exp(1)

    def get_pets(self):
        return self.pets
