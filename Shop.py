from AbilityManager import AbilityManager
from Pet import Pet
from Pet import PetAbility
from Team import Team
from SAP_Data import *
import random


class Shop:

    def __init__(self, team):
        self.team = team
        self.team.set_location(self)
        self.turn = 1
        self.turn_info = TURN_DATA.get("turn-" + str(self.turn))
        self.animal_shop_slots = self.turn_info.get("animalShopSlots")
        # self.food_shop_slots = self.turn_info.get("foodShopSlots")
        self.tiers_available = self.turn_info.get("tiersAvailable")
        self.can_bonus = 0
        self.shop_animals = [None, None, None]
        self.frozen_slots = [False, False, False, False, False]
        self.slot_selected = -1
        self.AM = AbilityManager(self)
        # self.shop_food = []

    def roll_shop(self):
        # shop_food = self.clear_non_frozen_food()
        # animals
        for i in range(0, self.animal_shop_slots):
            if not self.frozen_slots[i]:
                self.shop_animals[i] = self.random_shop_animal()
        # food
        # for i in range(len(shop_food), self.food_shop_slots):
        #     self.shop_food.append(self.random_shop_food())

    def random_shop_animal(self):
        possible_animals = []
        for i in range(self.tiers_available):
            possible_animals = possible_animals + AVAILABLE_ANIMALS[i]
        pet_tag = random.choice(possible_animals)
        pet = Pet(pet_tag[4:])
        pet.set_base_attack(pet.get_base_attack() + self.get_attack_bonus())
        pet.set_base_health(pet.get_base_health() + self.get_health_bonus())
        return pet

    # def random_shop_food(self):
    #     possible_foods = []
    #     for i in range(self.tiers_available):
    #         possible_foods = possible_foods + ANIMAL_TIERS[i]
    #     food_tag = random.choice(possible_foods)
    #     food = Food(food_tag[4:])
    #     return food

    def clear_non_frozen_animals(self):
        return [x for x in self.shop_animals if not x.get_is_frozen()]

    # def clear_non_frozen_food(self):
    #     return [x for x in self.shop_food if not x.get_is_frozen()]

    def get_team(self):
        return self.team

    def get_attack_bonus(self):
        return self.can_bonus

    def get_health_bonus(self):
        return self.can_bonus

    def get_all_pets(self):
        return self.team.get_pets()

    def get_enemy_team(self):
        return None

    def reset(self):
        self.turn = 1
        self.turn_info = TURN_DATA.get("turn-" + str(self.turn))
        self.animal_shop_slots = self.turn_info.get("animalShopSlots")
        self.tiers_available = self.turn_info.get("tiersAvailable")
        self.shop_animals = [None, None, None]

    def next_turn(self):
        self.turn += 1
        if self.turn <= 11:
            self.turn_info = TURN_DATA.get("turn-" + str(self.turn))
            self.tiers_available = self.turn_info.get("tiersAvailable")
            if self.turn == 5 or self.turn == 9:
                self.animal_shop_slots += 1
                self.shop_animals.append(None)

    def get_AM(self):
        return self.AM

    def get_turn(self):
        return self.turn

    def is_battleground(self):
        return False

    def is_shop(self):
        return True

    def get_slot_selected(self):
        return self.slot_selected

    def display(self):
        pass

