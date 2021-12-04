from functools import total_ordering
from AbilityManager import *
from SAP_Data import DATA
import random
from enum import Enum


class EFFECT_TYPE(Enum):
    AllOf = "AllOf"                                             # implemented
    ApplyStatus = "ApplyStatus"
    DealDamage = "DealDamage"                                   # implemented
    FoodMultiplier = "FoodMultiplier"
    GainExperience = "GainExperience"
    GainGold = "GainGold"
    ModifyStats = "ModifyStats"                                 # implemented
    ModifyStatsNotInBattle = "ModifyStatsNotInBattle"
    OneOf = "OneOf"                                             # implemented
    ReduceHealth = "ReduceHealth"
    RefillShops = "RefillShops"
    RepeatAbility = "RepeatAbility"
    SummonPet = "SummonPet"                                     # implemented
    SummonRandomPet = "SummonRandomPet"
    Swallow = "Swallow"
    TransferAbility = "TransferAbility"
    TransferStats = "TransferStats"


class TARGET(Enum):
    AdjacentAnimals = "AdjacentAnimals"                         # implemented
    All = "All"                                                 # implemented
    DifferentTierAnimals = "DifferentTierAnimals"               # implemented
    EachFriend = "EachFriend"                                   # implemented
    EachShopAnimal = "EachShopAnimal"                           # implemented
    FirstEnemy = "FirstEnemy"                                   # implemented
    FriendAhead = "FriendAhead"                                 # implemented
    FriendBehind = "FriendBehind"                               # implemented
    HighestHealthEnemy = "HighestHealthEnemy"                   # implemented
    LastEnemy = "LastEnemy"                                     # implemented
    LeftMostFriend = "LeftMostFriend"                           # implemented
    Level2And3Friends = "Level2And3Friends"                     # implemented
    LowestHealthEnemy = "LowestHealthEnemy"                     # implemented
    RandomEnemy = "RandomEnemy"                                 # implemented
    RandomFriend = "RandomFriend"                               # implemented
    RightMostFriend = "RightMostFriend"                         # implemented
    Self = "Self"                                               # implemented
    StrongestFriend = "StrongestFriend"                         # implemented
    TriggeringEntity = "TriggeringEntity"                       # implemented


# @total_ordering
class PetAbility:

    def __init__(self, pet, ability_data=None):

        self.pet = pet
        self.ability_data = ability_data
        self.name = self.pet.get_name_tag()
        self.level = self.pet.get_level()
        self.triggering_entity = None

        if self.ability_data is None:
            try:
                self.ability_data = DATA.get("pets").get(self.name).get("level" + str(self.level) + "Ability")
            except AttributeError:
                print("Error: the pet tag '" + self.name + "' does not exist!")
            self.description = self.ability_data.get("description")
            self.trigger = TRIGGER[self.ability_data.get("trigger")]
            self.triggered_by = TRIGGERED_BY[self.ability_data.get("triggeredBy").get("kind")]
            self.effect = self.ability_data.get("effect")
            self.effect_type = EFFECT_TYPE[self.effect.get("kind")]

        else:
            self.effect = ability_data
            self.effect_type = EFFECT_TYPE[self.ability_data.get("kind")]

    def execute(self):

        print("executing " + str(self.pet) + "'s ability")

        # if animal is fainted, then dont perform ability (unless the trigger is fainting itself)
        if self.pet.get_is_fainted():
            if not (self.trigger == TRIGGER.Faint and self.triggered_by == TRIGGERED_BY.Self):
                return

        if self.effect_type == EFFECT_TYPE.SummonPet:
            self.summon(self.triggering_entity)
            return

        if self.effect_type == EFFECT_TYPE.AllOf:
            self.all_of()
            return

        if self.effect_type == EFFECT_TYPE.OneOf:
            self.one_of()
            return

        # targeted abilities
        targets = self.generate_targets()

        if targets is None or all(x is None for x in targets):
            return

        # ModifyStats
        if self.effect_type == EFFECT_TYPE.ModifyStats:
            for target in targets:
                self.modify_stats(target)
                print(str(target) + " | gained stats!")
            return

        # DealDamage
        if self.effect_type == EFFECT_TYPE.DealDamage:
            for target in targets:
                self.deal_damage(target)
                print (str(self.pet) + " did damage to " + str(target))

    # generates the list of targets for the ability when it is triggered

    def generate_targets(self):
        target_info = None

        target_info = self.effect.get("target")

        if target_info is None:
            return

        team = copy.copy(self.pet.get_battleground_team().get_pets())
        if team is None:
            team = copy.copy(self.pet.get_team().get_pets())

        enemy_team = copy.copy(self.pet.get_battleground_enemy_team().get_pets())

        targets = []

        kind = TARGET[target_info.get("kind")]

        # Self
        if kind == TARGET.Self:
            targets.append(self.pet)
            return targets

        # TriggeringEntity
        if kind == TARGET.TriggeringEntity:
            targets.append(self.triggering_entity)
            return targets

        # RandomFriend
        if kind == TARGET.RandomFriend:
            n = target_info.get("n")
            # pprint(friends)
            try:
                team.remove(self.pet)
            except ValueError:
                pass
            n = min(n, len(team))
            targets = random.sample(team, n)
            return targets

        # RandomEnemy
        if kind == TARGET.RandomEnemy:
            n = target_info.get("n")
            n = max(n, len(enemy_team))
            targets = random.sample(enemy_team, n)
            return targets

        # All
        if kind == TARGET.All:
            targets.append(team)
            if enemy_team is not None:
                targets.append(enemy_team)
            return targets

        # AdjacentAnimals only in battleground (for now)
        if kind == TARGET.AdjacentAnimals:

            team1 = []
            team2 = []

            for x in team:
                team1.append(x)

            for x in enemy_team:
                team2.insert(0, x)

            targets_list = team1
            targets_list.append(team2)

            index = targets_list.index(self.pet)

            target1 = None
            target1_index = index-1
            while target1_index >= 0 and target1 is None:
                target1 = targets_list[target1_index]
                target1_index -= 1

            target2 = None
            target2_index = index + 1
            while target2_index <= 9 and target2 is None:
                target2 = targets_list[target1_index]
                target2_index += 1

            targets.append([target1, target2])
            return targets

        # DifferentTierAnimals
        if kind == TARGET.DifferentTierAnimals:
            for x in team.append(enemy_team):
                if not x.get_tier() == self.pet.get_tier():
                    targets.append(x)
            return targets

        # EachFriend
        if kind == TARGET.EachFriend:
            try:
                team.remove(self.pet)
            except ValueError:
                pass
            return team

        # EachShopAnimal
        if kind == TARGET.EachShopAnimal:
            return None
            # not implemented

        # FirstEnemy
        if kind == TARGET.FirstEnemy:
            for target in enemy_team:
                if target is not None:
                    targets.append(target)
                    return targets

        # FriendAhead
        if kind == TARGET.FriendAhead:
            for i in range(team.index(self.pet) + 1, 5):
                if team[i] is not None:
                    targets.append(team[i])
                    return targets

        # FriendBehind
        if kind == TARGET.FriendBehind:
            target = None
            i = team.index(self.pet)-1
            while i >= 0 and target is None:
                target = team[i]
                i -= 1
            targets.append(target)
            return targets

        # HighestHealthEnemy
        if kind == TARGET.HighestHealthEnemy:
            target = None
            for x in enemy_team:
                if target is None:
                    target = x
                elif x is not None and x.get_health() > target.get_health():
                    target = x
            targets.append(target)
            return targets

        # LastEnemy
        if kind == TARGET.LastEnemy:
            for x in enemy_team:
                if x is not None:
                    targets.append(x)
                    return targets

        # LeftMostFriend
        if kind == TARGET.LeftMostFriend:
            for i in range(5):
                if team[i] is not None:
                    targets.append(team[i])
                    return targets

        # Level2And3Friends
        if kind == TARGET.Level2And3Friends:
            for x in team:
                if x is not None and x.get_level() >= 2:
                    targets.append(x)
            return targets

        # LowestHealthEnemy
        if kind == TARGET.LowestHealthEnemy:
            target = None
            for x in enemy_team:
                if target is None:
                    target = x
                elif x is not None and x.get_health() < target.get_health():
                    target = x
            targets.append(target)
            return targets

        # RightMostFriend
        if kind == TARGET.RightMostFriend:
            for i in range(5):
                if team[4 - i] is not None:
                    targets.append(team[4 - i])
                    return targets

        # StrongestFriend
        if kind == TARGET.StrongestFriend:
            target = None
            for x in team:
                if target is None:
                    target = x
                elif x is not None and x.get_health() + x.get_attack < target.get_health() + target.get_attack():
                    target = x
            targets.append(target)
            return targets

    def modify_stats(self, target):
        stats = [0, 0]
        try:
            stats[0] = self.effect.get("attackAmount")
        except AttributeError:
            pass
        try:
            stats[1] = self.effect.get("healthAmount")
        except AttributeError:
            pass
        if stats[0] is None:
            stats[0] = 0
        if stats[1] is None:
            stats[1] = 0
        target.gain_stats(stats, 0)

    def deal_damage(self, target):

        damage = 0
        try:
            damage = self.effect.get("amount")
        except AttributeError:
            pass
        target.take_damage(self.pet, damage)

    def summon(self, target):

        n = self.ability_data.get("effect").get("n")
        summon_team = self.ability_data.get("effect").get("team")
        summon_tag = self.ability_data.get("effect").get("pet")
        summon_tag = summon_tag[4:]
        summon_attack = self.ability_data.get("effect").get("withAttack")
        summon_health = self.ability_data.get("effect").get("withHealth")

        team = self.pet.get_battleground_team()
        if team is None:
            team = self.pet.get_team()

        if summon_team == "Enemy":
            team = self.pet.get_battleground_enemy_team()

        if team is None:
            return

        target_index = team.get_pets().index(target)

        for i in range(n):
            team.summon_pet(target_index, summon_tag, summon_attack, summon_health)

    def all_of(self):
        for ability_data in self.ability_data.get("effect").get("effects"):
            to_run = PetAbility(self.pet, ability_data)
            to_run.execute()

    def one_of(self):
        ability_data = random.sample(self.ability_data.get("effect").get("effects"), 1)
        to_run = PetAbility(self.pet, ability_data[0])
        to_run.execute()

    # def __eq__(self, other):
    #     return self.pet.get_attack() == other.pet.get_attack()

    # def __gt__(self, other):
    #     return self.pet.get_attack() > other.pet.get_attack()

    # getters and setters
    def get_trigger(self):
        return self.trigger

    def get_triggered_by(self):
        return self.triggered_by
