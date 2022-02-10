from Pet import Pet, generate_random_pet
from SAP_Data import *
from RandomName import *
from AbilityManager import *


t_f_list = [0, 1]


class Team:

    def __init__(self, input_name, plural):

        # initialize default team
        self.pets = [None] * 5  # Type : Pets
        self.lives = 10
        self.wins = 0
        self.turn = TURN_DATA.get("turn-1")
        self.battleground = None
        self.name = input_name
        self.plural = plural

    def add_pet(self, new_pet, pos):
        if self.pets[pos] is None:
            self.pets[pos] = new_pet
        else:
            print("that position is taken")
            return -1
        new_pet.set_team(self)

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
                    if get_debug_mode():
                        print(str(summon_animal) + " was summoned with status: " + str(status))
                    has_summoned = True
                else:
                    self.advance_team_from(index)
                    x = self.pets[index]
                    if x is None:
                        self.pets[index] = summon_animal
                        send_triggers(TRIGGER.Summoned, summon_animal, self.battleground)
                        if get_debug_mode():
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
        for j in range(4 - index):
            if self.pets[4 - j] is None:
                self.pets[4 - j] = self.pets[3 - j]
                self.pets[3 - j] = None

    def retreat_team(self):
        for j in range(4):
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

    def get_pets(self):
        return self.pets

    def get_name(self):
        return self.name

    def is_plural(self):
        return self.plural

    def set_battleground(self, bg):
        self.battleground = bg

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
            new_pet.set_status(random.choice(list(STATUS)))

    def copy_team(self, team_to_copy):
        self.pets = team_to_copy.pets # Type : Pets
        self.lives = team_to_copy.lives
        self.wins = team_to_copy.wins
        self.turn = TURN_DATA.get("turn-1")
        self.battleground = None
        self.name = team_to_copy.name
        self.plural = team_to_copy.plural

    # def __str__(self):
    #     team_string = []
    #     for pet in self.pets:
    #         team_string.append(pet.get_name_tag())
    #     return str(team_string)
