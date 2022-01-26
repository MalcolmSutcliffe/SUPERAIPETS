from Pet import Pet
from Pet import PetAbility
from Team import Team
from SAP_Data import DATA, ANIMAL_TIERS
import random


class Shop:

    def __init__(self, team, turn=1):
        self.team = team
        self.turn = turn
        self.turn_info = DATA.get("turns").get("turn-" + str(self.turn))
        self.animal_shop_slots = self.turn_info.get("animalShopSlots")
        self.food_shop_slots = self.turn_info.get("foodShopSlots")
        self.tiers_available = self.turn_info.get("tiersAvailable")
        self.can_bonus = 0
        self.shop_animals = []
        self.shop_food = []

    def roll_shop(self):
        shop_animals = self.clear_non_frozen_animals()
        shop_food =  self.clear_non_frozen_food()
        # animals
        for i in range(len(shop_animals), self.animal_shop_slots):
            self.shop_animals.append(self.random_shop_animal())
        # food
        for i in range(len(shop_food), self.food_shop_slots):
            self.shop_food.append(self.random_shop_food())

    def random_shop_animal(self):
        possible_animals = []
        for i in range(self.tiers_available):
            possible_animals = possible_animals + ANIMAL_TIERS[i]
        pet_tag = random.choice(possible_animals)
        pet = Pet(pet_tag[4:])
        pet.set_base_attack(pet.get_base_attack() + self.get_attack_bonus())
        pet.set_base_health(pet.get_base_health() + self.get_health_bonus())
        return pet

    def random_shop_food(self):
        possible_foods = []
        for i in range(self.tiers_available):
            possible_foods = possible_foods + ANIMAL_TIERS[i]
        food_tag = random.choice(possible_foods)
        # food = Food(food_tag[4:])
        return

    def clear_non_frozen_animals(self):
        return [x for x in self.shop_animals if not x.get_is_frozen()]

    def clear_non_frozen_food(self):
        return [x for x in self.shop_food if not x.get_is_frozen()]

    def get_attack_bonus(self):
        return self.can_bonus

    def get_health_bonus(self):
        return self.can_bonus
