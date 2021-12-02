import json
from functools import total_ordering
from pprint import pprint

from AbilityManager import *
from SAP_Data import DATA
import random
from enum import Enum


class EFFECT_TYPE(Enum):
    AllOf = "AllOf"
    ApplyStatus = "ApplyStatus"
    DealDamage = "DealDamage"
    FoodMultiplier = "FoodMultiplier"
    GainExperience = "GainExperience"
    GainGold = "GainGold"
    ModifyStats = "ModifyStats"
    OneOf = "OneOf"
    ReduceHealth = "ReduceHealth"
    RefillShops = "RefillShops"
    RepeatAbility = "RepeatAbility"
    SummonPet = "SummonPet"
    SummonRandomPet = "SummonRandomPet"
    Swallow = "Swallow"
    TransferAbility = "TransferAbility"
    TransferStats = "TransferStats"


class TARGET(Enum):
    AdjacentAnimals = "AdjacentAnimals"
    All = "All"
    DifferentTierAnimals = "DifferentTierAnimals"
    EachFriend = "EachFriend"
    EachShopAnimal = "EachShopAnimal"
    FirstEnemy = "FirstEnemy"
    FriendAhead = "FriendAhead"
    FriendBehind = "FriendBehind"
    HighestHealthEnemy = "HighestHealthEnemy"
    LastEnemy = "LastEnemy"
    LeftMostFriend = "LeftMostFriend"
    Level2And3Friends = "Level2And3Friends"
    LowestHealthEnemy = "LowestHealthEnemy"
    RandomEnemy = "RandomEnemy"  # n needed
    RandomFriend = "RandomFriend"  # n needed
    RightMostFriend = "RightMostFriend"
    Self = "Self"
    StrongestFriend = "StrongestFriend"
    TriggeringEntity = "TriggeringEntity"


# @total_ordering
class PetAbility:

    def __init__(self, pet):

        self.pet = pet
        self.ability_data = None
        self.name = self.pet.get_name_tag()
        self.level = self.pet.get_level()

        try:
            self.ability_data = DATA.get("pets").get(self.name).get("level" + str(self.level) + "Ability")
        except AttributeError:
            print("Error: the pet tag '" + self.name + "' does not exist!")

        self.description = self.ability_data.get("description")
        self.trigger = TRIGGER[self.ability_data.get("trigger")]
        self.triggered_by = TRIGGERED_BY[self.ability_data.get("triggeredBy").get("kind")]
        self.effect_type = EFFECT_TYPE[self.ability_data.get("effect").get("kind")]

    def execute(self):

        # Modify Stats
        if self.effect_type == EFFECT_TYPE.ModifyStats:
            targets = self.generate_targets()
            for target in targets:
                self.modify_stats(target)
                print(str(target) + " | gained stats!")

    # generates the list of targets for the ability when it is triggered

    def generate_targets(self):
        target_info = None
        try:
            target_info = self.ability_data.get("effect").get("target")
        except AttributeError:
            print("error: the ability is not a targeted ability")
            return

        kind = TARGET[target_info.get("kind")]

        if kind == TARGET.RandomFriend:
            n = target_info.get("n")
            if self.pet.get_battleground_team() is None:
                friends = copy.copy(self.pet.get_team())
            else:
                friends = copy.copy(self.pet.get_battleground_team())
            # pprint(friends)
            try:
                friends.remove(self)
            except ValueError:
                print("ok")
            n = min(n, len(friends))
            targets = random.sample(friends, n)
            return targets

        if kind == TARGET.RandomEnemy:
            n = target_info.get("n")
            if self.pet.get_battleground_team() is None:
                return
            else:
                enemies = self.pet.get_battleground_enemy_team()
            n = max(n, len(enemies))
            targets = random.sample(enemies, n)
            return targets

    def modify_stats(self, target):
        stats = [0, 0]
        try:
            stats[0] = self.ability_data.get("effect").get("attackAmount")
        except AttributeError:
            stats[0] = 0
        try:
            stats[1] = self.ability_data.get("effect").get("healthAmount")
        except AttributeError:
            stats[1] = 0

        target.gain_stats(stats, 0)

    # def __eq__(self, other):
    #     return self.pet.get_attack() == other.pet.get_attack()

    # def __gt__(self, other):
    #     return self.pet.get_attack() > other.pet.get_attack()

    # getters and setters
    def get_trigger(self):
        return self.trigger

    def get_triggered_by(self):
        return self.triggered_by
