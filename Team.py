import copy

from Pet import Pet, generate_random_pet
from SAP_Data import *
from RandomName import *
from AbilityManager import *

t_f_list = [0, 1]


class Team:

    def __init__(self, input_name="default_name", plural=False, location=None):

        # initialize default team

        self.pets = [None] * 5
        self.lives = 10
        self.wins = 0
        self.turn = TURN_DATA.get("turn-1")
        self.name = input_name
        self.plural = plural
        self.location = location

    def add_pet(self, new_pet, pos):
        if self.pets[pos] is None:
            self.pets[pos] = new_pet
            new_pet.set_team(self)
            if self.location is not None:
                self.location.get_AM().send_triggers(TRIGGER.Summoned, new_pet)
        else:
            print("that position is taken")
            return -1

    def summon_pet(self, index, summon_tag, summon_attack=0, summon_health=0, level=1, status=None, n=1):
        for j in range(n):
            summon_animal = Pet(summon_tag)
            summon_animal.generate_ability()

            summon_animal.set_team(self)

            summon_animal.set_base_attack(summon_attack)
            summon_animal.set_base_health(summon_health)
            summon_animal.set_status(status)
            summon_animal.set_level(level)

            self.remove_fainted()
            self.location.display()

            def attempt_summon(pos, pet):
                if self.pets[pos] is None:
                    self.add_pet(pet, pos)
                    if get_debug_mode():
                        print(str(pet) + " was summoned with status: " + str(status))
                    return True
                else:
                    return False

            if self.has_space():
                self.location.display()
                self.advance_team_from(index)
                if attempt_summon(index, summon_animal):
                    return
                self.retreat_team_from(index)
                if attempt_summon(index, summon_animal):
                    return
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
        self.advance_team_from(0)

    def advance_team_from(self, index):
        # loop from front (4) to index
        for j in range(4 - index):
            # if empty position, advance unit up
            if self.pets[4 - j] is None:
                self.pets[4 - j] = self.pets[3 - j]
                self.pets[3 - j] = None

    def retreat_team(self):
        self.retreat_team_from(4)

    def retreat_team_from(self, index):
        # loop from back (0) to index
        for j in range(index - 1):
            # if empty, retreat
            if self.pets[j] is None:
                self.pets[j] = self.pets[j + 1]
                self.pets[j + 1] = None

    def remove_fainted(self):
        for (j, x) in enumerate(self.pets):
            if x is not None:
                if x.get_is_fainted():
                    self.pets[j] = None

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

    # returns shallow copy of pets
    def get_pets(self):
        return copy.copy(self.pets)

    def get_name(self):
        return self.name

    def is_plural(self):
        return self.plural

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_enemy_team(self):
        return self.location.get_enemy_team(self)

    def set_name(self, name_string, plural):
        self.name = name_string

    def reset(self, input_name, plural):
        self.pets = [None] * 5  # Type : Pets
        self.lives = 10
        self.wins = 0
        self.turn = TURN_DATA.get("turn-1")
        self.name = input_name
        self.plural = plural

    def randomize_team(self):
        plural = random.choice(t_f_list)
        if plural == 0:
            self.reset(generateRandomNameSingular(), False)
        else:
            self.reset(generateRandomNamePlural(), True)
        for j in range(5):
            new_pet = generate_random_pet()
            new_pet.set_level(random.randint(1, 3))
            self.add_pet(new_pet, j)
            if random.uniform(0, 1) > 0.7:
                new_pet.set_status(random.choice(list(STATUS)))

    def deep_copy(self):
        new_team = copy.copy(self)
        new_pets = copy.copy(self.pets)
        for j, x in enumerate(new_pets):
            if isinstance(x, Pet):
                new_pet = x.deep_copy()
                new_pet.set_team(new_team)
                new_pets[j] = new_pet
        new_team.pets = new_pets
        return new_team

    # def __str__(self):
    #     team_string = []
    #     for pet in self.pets:
    #         team_string.append(pet.get_name_tag())
    #     return str(team_string)
