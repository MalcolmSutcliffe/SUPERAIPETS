import copy
from functools import total_ordering
from AbilityManager import *
from SAP_Data import DATA, ANIMAL_TIERS
from Status import STATUS
import random
from enum import Enum


class EFFECT_TYPE(Enum):
    AllOf = 1  # implemented
    ApplyStatus = 2  # implemented
    DealDamage = 3  # implemented
    FoodMultiplier = 4
    GainExperience = 5
    GainGold = 6
    ModifyStats = 7  # implemented
    ModifyStatsNotInBattle = 8
    OneOf = 9  # implemented
    ReduceHealth = 10  #
    RefillShops = 11
    RepeatAbility = 12  #
    SummonPet = 13  # implemented
    SummonRandomPet = 14  #
    Swallow = 15  #
    TransferAbility = 16
    TransferStats = 17  #


class TARGET(Enum):
    AdjacentAnimals = 1  # implemented
    All = 2  # implemented
    DifferentTierAnimals = 3  # implemented
    EachFriend = 4  # implemented
    EachShopAnimal = 5  # implemented
    FirstEnemy = 6  # implemented
    FriendAhead = 7  # implemented
    FriendBehind = 8  # implemented
    HighestHealthEnemy = 9  # implemented
    LastEnemy = 10  # implemented
    LeftMostFriend = 11  # implemented
    Level2And3Friends = 12  # implemented
    LowestHealthEnemy = 13  # implemented
    RandomEnemy = 14  # implemented
    RandomFriend = 15  # implemented
    RightMostFriend = 16  # implemented
    Self = 17  # implemented
    StrongestFriend = 18  # implemented
    TriggeringEntity = 19  # implemented


@total_ordering
class PetAbility:

    def __init__(self, pet, ability_data=None):

        self.pet = pet
        self.ability_data = ability_data
        self.name = self.pet.get_name_tag()
        self.level = self.pet.get_level()
        self.triggering_entity = None
        self.priority = 0

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

        if self.effect_type == EFFECT_TYPE.DealDamage:
            self.priority = 1

    def execute(self):

        # if animal is fainted, then dont perform ability (unless the trigger is fainting itself)
        if self.pet.get_is_fainted():
            if not (self.trigger == TRIGGER.Faint and self.triggered_by == TRIGGERED_BY.Self):
                return

        # AllOf
        if self.effect_type == EFFECT_TYPE.AllOf:
            self.all_of()
            return

        # OneOf
        if self.effect_type == EFFECT_TYPE.OneOf:
            self.one_of()
            return

        print(str(self.pet) + " used their " + str(self.effect_type) + " ability!")

        # SummonPet
        if self.effect_type == EFFECT_TYPE.SummonPet:
            self.summon(self.triggering_entity, False)
            return

        # SummonRandomPet
        if self.effect_type == EFFECT_TYPE.SummonRandomPet:
            self.summon(self.triggering_entity, True)
            return

        # targeted abilities
        targets = self.generate_targets()

        if targets is None or all(x is None for x in targets):
            return

        # ModifyStats
        if self.effect_type == EFFECT_TYPE.ModifyStats:
            for target in targets:
                self.modify_stats(target)
            return

        # DealDamage
        if self.effect_type == EFFECT_TYPE.DealDamage:
            for target in targets:
                print(str(self.pet) + " did damage to " + str(target))
                self.deal_damage(target)
            return

        # ApplyStatus
        if self.effect_type == EFFECT_TYPE.ApplyStatus:
            for target in targets:
                self.apply_status(target)
            return

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
            targets = copy.copy(enemy_team)
            for x in targets:
                if x.get_is_fainted():
                    targets.remove(x)
            n = min(n, len(targets))
            targets = random.sample(targets, n)
            return targets

        # All
        if kind == TARGET.All:
            targets.append(team)
            if enemy_team is not None:
                targets.append(enemy_team)
            return targets

        # AdjacentAnimals only in battleground (for now)
        if kind == TARGET.AdjacentAnimals:

            targets_list = self.pet.get_battleground().get_all_pets()

            index = targets_list.index(self.pet)

            target1_index = index - 1
            while target1_index >= 0:
                x = targets_list[target1_index]
                if x is not None:
                    targets.append(x)
                    break
                target1_index -= 1

            target2_index = index + 1
            while target2_index <= 9:
                x = targets_list[target2_index]
                if x is not None:
                    targets.append(x)
                    break
                target1_index += 1

            print("adjacent enemies:")
            for x in targets:
                print(x)
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
            targets = [i for i in enemy_team if i is not None and not i.get_is_fainted()]
            if len(targets) > 0:
                return [targets[len(targets)-1]]
            return

        # FriendAhead
        if kind == TARGET.FriendAhead:
            n = target_info.get("n")
            for i in range(n):
                for j in range(team.index(self.pet) + 1 + i, 5):
                    if j <= 4 and team[j] is not None:
                        targets.append(team[j])
                        break
            return targets

        # FriendBehind
        if kind == TARGET.FriendBehind:
            n = target_info.get("n")
            for i in range(n):
                for j in range(1 + i, 5):
                    if 4 - j >= 0 and team[4 - j] is not None:
                        targets.append(team[4 - j])
                        break
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

        try:
            multiplier = damage.get("multiplier")
            damage = int(self.pet.get_attack() * multiplier)
        except AttributeError:
            pass

        target.take_damage(self.pet, damage)

    def summon(self, target, summon_random):

        if not summon_random:
            summon_tag = self.effect.get("pet")
            n = self.effect.get("n")
            summon_team = self.effect.get("team")
        else:
            tier = self.effect.get("tier")
            summon_tag = random.sample(ANIMAL_TIERS[tier - 1], 1)[0]
            n = 1
            summon_team = "Friendly"

        summon_tag = summon_tag[4:]
        summon_attack = self.effect.get("withAttack")
        summon_health = self.effect.get("withHealth")

        if summon_attack is None:
            summon_attack = DATA.get("pets").get(summon_tag).get("baseAttack")
        if summon_health is None:
            summon_health = DATA.get("pets").get(summon_tag).get("baseHealth")

        try:
            status = STATUS[self.effect.get("withStatus")]
        except KeyError:
            status = None

        team = self.pet.get_battleground_team()
        if team is None:
            team = self.pet.get_team()

        if summon_team == "Enemy":
            team = self.pet.get_battleground_enemy_team()

        if team is None:
            return

        target_index = team.get_pets().index(target)

        if n is None:
            n = 1

        for i in range(n):
            team.summon_pet(target_index, summon_tag, summon_attack, summon_health, 1, status)

    def all_of(self):
        for ability_data in self.effect.get("effects"):
            to_run = PetAbility(self.pet, ability_data)
            to_run.execute()

    def one_of(self):
        ability_data = random.sample(self.effect.get("effects"), 1)
        to_run = PetAbility(self.pet, ability_data[0])
        to_run.execute()

    def apply_status(self, target):
        status = STATUS[self.effect.get("status")]
        target.set_status(status)

    def __eq__(self, other):
        return self.priority == other.priority and self.pet.get_attack() == other.pet.get_attack()

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.pet.get_attack() > other.pet.get_attack()
        else:
            return self.priority < other.priority

    # getters and setters
    def get_trigger(self):
        return self.trigger

    def get_triggered_by(self):
        return self.triggered_by

    def __str__(self):
        return str(self.pet) + " " + str(self.effect_type) + " " + str(self.trigger)