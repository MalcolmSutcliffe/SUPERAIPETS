import copy
import random
from functools import total_ordering
from SAP_Data import *


# -----------------------
# | Targeting Functions |
# -----------------------

# Self
def target_self(pet_ability):
    pet_ability.targets = [pet_ability.pet]


# TriggeringEntity
def target_triggering_entity(pet_ability):
    pet_ability.targets = [pet_ability.triggering_entity]


# RandomFriend
def target_random_friend(pet_ability):
    n = pet_ability.target_info.get("n")
    targets = pet_ability.pet.get_team().get_pets()

    try:
        targets.remove(pet_ability.pet)
    except ValueError:
        pass

    # remove blanks or fainted from the list
    targets = [x for x in targets if x is not None]
    targets = [x for x in targets if not x.get_is_fainted()]
    n = min(n, len(targets))
    targets = random.sample(targets, n)
    pet_ability.targets = targets


# RandomEnemy
def target_random_enemy(pet_ability):
    n = pet_ability.target_info.get("n")
    enemy_team = pet_ability.pet.get_enemy_team()
    if enemy_team is None:
        pet_ability.targets = []
        return
    targets = enemy_team.get_pets()
    targets = [x for x in targets if x is not None]
    targets = [x for x in targets if not x.get_is_fainted()]
    n = min(n, len(targets))
    targets = random.sample(targets, n)
    pet_ability.targets = targets


# All
def target_all(pet_ability):
    team = pet_ability.pet.get_team()
    enemy_team = pet_ability.pet.get_enemy_team()
    targets = []
    for x in team.get_pets():
        if x is not None:
            targets.append(x)
    if enemy_team is not None:
        for x in enemy_team.get_pets():
            if x is not None:
                targets.append(x)
    pet_ability.targets = targets


# AdjacentAnimals
def target_adjacent_animals(pet_ability):
    targets_list = pet_ability.pet.get_location().get_all_pets()
    index = targets_list.index(pet_ability.pet)
    targets = []

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

    pet_ability.targets = targets


# DifferentTierAnimals
def target_different_tier_animals(pet_ability):
    team = pet_ability.pet.get__team().get_pets()
    enemy_team = pet_ability.pet.get_enemy_team().get_pets()
    targets = []
    for x in team.append(enemy_team):
        if not x.get_tier() == pet_ability.pet.get_tier():
            targets.append(x)
    pet_ability.targets = targets


# EachFriend
def target_each_friend(pet_ability):
    targets = pet_ability.pet.get_team().get_pets()
    try:
        targets.remove(pet_ability.pet)
    except ValueError:
        pass
    pet_ability.targets = targets


# EachEnemy
def target_each_enemy(pet_ability):
    targets = pet_ability.pet.get_enemy_team().get_pets()
    pet_ability.targets = targets


# EachShopAnimal (not implemented)
# def target_each_shop_animal(pet_ability):
#     return None
#     # not implemented

# FirstEnemy
def target_first_enemy(pet_ability):
    enemy_team = pet_ability.pet.get_enemy_team().get_pets()
    targets = [j for j in enemy_team if j is not None and not j.get_is_fainted()]
    if len(targets) > 0:
        targets = [targets[len(targets) - 1]]
    pet_ability.targets = targets


# FriendAhead
def target_friend_ahead(pet_ability):
    team = pet_ability.pet.get_team().get_pets()
    n = pet_ability.target_info.get("n")
    team = [j for j in team if j is not None]
    team = [j for j in team if not j.get_is_fainted()]
    targets = []
    for k in range(n):
        for j in range(team.index(pet_ability.pet) + 1, 5):
            if j < len(team) and team[j] is not None and targets.count(team[j]) == 0:
                targets.append(team[j])
                break
    pet_ability.targets = targets


# FriendBehind
def target_friend_behind(pet_ability):
    team = pet_ability.pet.get_team().get_pets()
    n = pet_ability.target_info.get("n")
    targets = []
    for k in range(n):
        index = team.index(pet_ability.pet)
        for j in range(1, index):
            if index - j >= 0 and team[index - j] is not None and targets.count(team[index - j]) == 0:
                targets.append(team[index - j])
                break
    pet_ability.targets = targets


# HighestHealthEnemy
def target_highest_health_enemy(pet_ability):
    enemy_team = pet_ability.pet.get_enemy_team().get_pets()
    target = None
    for x in enemy_team:
        if target is None:
            target = x
        elif x is not None and x.get_health() > target.get_health():
            target = x
    pet_ability.targets = [target]


# LastEnemy
def target_last_enemy(pet_ability):
    enemy_team = pet_ability.pet.get_enemy_team().get_pets()
    for x in enemy_team:
        if x is not None and not x.get_is_fainted():
            pet_ability.targets = [x]
            return


# LeftMostFriend
def target_left_most_friend(pet_ability):
    team = pet_ability.pet.get_team().get_pets()
    for k in range(5):
        if team[k] is not None:
            pet_ability.targets = [team[k]]
            return


# Level2And3Friends
def target_level_2_and_3_friends(pet_ability):
    team = pet_ability.pet.get_team().get_pets()
    targets = []
    for x in team:
        if x is not None and x.get_level() >= 2:
            targets.append(x)
    pet_ability.targets = targets


# LowestHealthEnemy
def target_lowest_health_enemy(pet_ability):
    enemy_team = pet_ability.pet.get_enemy_team().get_pets()
    target = None
    for x in enemy_team:
        if target is None:
            target = x
        elif x is not None and x.get_health() < target.get_health() and not x.get_is_fainted():
            target = x
    pet_ability.targets = [target]


# RightMostFriend
def target_right_most_friend(pet_ability):
    team = pet_ability.pet.get_team().get_pets()
    for k in range(5):
        if team[4 - k] is not None:
            pet_ability.targets = [team[4 - k]]


# StrongestFriend
def target_strongest_friend(pet_ability):
    team = pet_ability.pet.get_team().get_pets()
    target = None
    for x in team:
        if target is None:
            target = x
        elif x is not None and x.get_health() + x.get_attack() > target.get_health() + target.get_attack():
            target = x
    pet_ability.targets = [target]


# ---------------------
# | Ability Functions |
# ---------------------

# ModifyStats
def modify_stats(pet_ability):
    stats = [0, 0]
    multiplier = 1
    until_end_of_battle = False

    try:
        stats[0] = pet_ability.effect.get("attackAmount")
    except AttributeError:
        pass
    try:
        stats[1] = pet_ability.effect.get("healthAmount")
    except AttributeError:
        pass
    try:
        until_end_of_battle = pet_ability.effect.get("untilEndOfBattle")
    except AttributeError:
        pass
    try:
        multiplier = pet_ability.effect.get("multiplier")
    except AttributeError:
        pass

    if stats[0] == "this":
        stats[0] = pet_ability.pet.get_attack()

    if stats[0] is None:
        stats[0] = 0
    if stats[1] is None:
        stats[1] = 0
    if multiplier is None:
        multiplier = 1

    stats[0] = stats[0] * multiplier
    stats[1] = stats[1] * multiplier

    pet_ability.generate_targets()

    for target in pet_ability.targets:
        target.gain_stats(stats, until_end_of_battle)


# DealDamage
def deal_damage(pet_ability):
    damage = 0
    try:
        damage = pet_ability.effect.get("amount")
    except AttributeError:
        pass

    try:
        multiplier = damage.get("multiplier")
        damage = int(pet_ability.pet.get_attack() * multiplier)
    except AttributeError:
        pass

    pet_ability.generate_targets()

    for target in pet_ability.targets:
        target.take_damage(pet_ability.pet, damage)


# Summon
def summon_pet(pet_ability):
    if not pet_ability.summon_random:
        summon_tag = pet_ability.effect.get("pet")
        n = pet_ability.effect.get("n")
    else:
        tier = pet_ability.effect.get("tier")
        summon_tag = random.sample(AVAILABLE_ANIMALS[tier - 1], 1)[0]
        n = 1

    summon_tag = summon_tag[4:]
    summon_attack = pet_ability.effect.get("withAttack")
    summon_health = pet_ability.effect.get("withHealth")

    if summon_attack != "this":
        pass
    else:
        summon_attack = pet_ability.pet.get_attack()

    if summon_attack is None:
        summon_attack = PET_DATA.get("pet-" + summon_tag).get("baseAttack")
    if summon_health is None:
        summon_health = PET_DATA.get("pet-" + summon_tag).get("baseHealth")

    try:
        status = STATUS[pet_ability.effect.get("withStatus")]
    except KeyError:
        status = None

    level = pet_ability.effect.get("withLevel")

    if level is None:
        level = 1

    pet_ability.generate_targets()
    target = pet_ability.targets[0]

    if target.get_name_tag()[4:] == summon_tag:
        return

    if n is None:
        n = 1

    for j in range(n):
        index = target.get_index()
        if index >= 0:
            target.get_team().summon_pet(target.get_index(), summon_tag, summon_attack, summon_health, level, status, n)


# SummonRandomPet
def summon_random_pet(pet_ability):
    pet_ability.summon_random = True
    summon_pet(pet_ability)


# AllOf
def all_of(pet_ability):
    for ability_data in pet_ability.effect.get("effects"):
        to_run = PetAbility(pet_ability.pet, ability_data)
        to_run.execute()


# OneOf
def one_of(pet_ability):
    ability_data = random.sample(pet_ability.effect.get("effects"), 1)
    to_run = PetAbility(pet_ability.pet, ability_data[0])
    to_run.execute()


# ApplyStatus
def apply_status(pet_ability):
    status = STATUS[pet_ability.effect.get("status")]

    pet_ability.generate_targets()

    for target in pet_ability.targets:
        target.set_status(status)


# RepeatAbility
def repeat_ability(pet_ability):
    n = pet_ability.effect.get("n")
    for j in range(n):

        pet_ability.generate_targets()

        for target in pet_ability.targets:
            target.get_location().AM.add_to_queue(target.get_ability())


# ReduceHealth
def reduce_health(pet_ability):
    percent = pet_ability.effect.get("percentage")

    pet_ability.generate_targets()

    for target in pet_ability.targets:
        if get_debug_mode():
            print(str(pet_ability.pet) + " reduced " + str(target) + "'s health by " + str(percent * 100) + "%")
        new_health = int(target.get_health() * (1 - percent))
        if new_health <= 0:
            new_health = 1
        target.set_health(new_health)


# Swallow
def swallow(pet_ability):
    pet_ability.trigger = TRIGGER.Faint
    pet_ability.triggered_by = TRIGGERED_BY.Self
    pet_ability.effect_type = EFFECT_TYPE.SummonPet

    pet_ability.generate_targets()

    target = pet_ability.targets[0]
    target.faint()
    pet_ability.effect = \
        {"kind": "SummonPet",
         "pet": target.get_name_tag(),
         "team": "Friendly",
         "withHealth": 1,
         "withAttack": 1,
         "withLevel": pet_ability.level,
         "target": {
             "kind": "Self"
         }
         }


# Evolve
def evolve(pet_ability):
    summon_attack = pet_ability.effect.get("withAttack")
    summon_health = pet_ability.effect.get("withHealth")
    status = None
    level = 1

    summon_tag = pet_ability.effect.get("into")
    summon_tag = summon_tag[4:]

    if summon_attack == "this":
        summon_attack = pet_ability.pet.get_attack()

    if summon_attack is None:
        summon_attack = PET_DATA.get("pet-" + summon_tag).get("baseAttack")
    if summon_health is None:
        summon_health = PET_DATA.get("pet-" + summon_tag).get("baseHealth")

    team = pet_ability.pet.get_team()
    if team is None:
        team = pet_ability.pet.get_team()

    if team is None:
        return
    try:
        target_index = team.get_pets().index(pet_ability.pet)
    except ValueError:
        target_index = 4

    pet_ability.pet.faint()

    team.summon_pet(target_index, summon_tag, summon_attack, summon_health, level, status)


# TransferStats
def transfer_stats(pet_ability):
    copy_attack = pet_ability.effect.get("copyAttack")
    copy_health = pet_ability.effect.get("copyHealth")
    pet_ability.target_info = pet_ability.effect.get("from")
    pet_ability.generate_targets()
    if not pet_ability.targets:
        return
    pet_from = pet_ability.targets
    pet_ability.target_info = pet_ability.effect.get("to")
    pet_ability.generate_targets()
    if not pet_ability.targets:
        return
    pet_to = pet_ability.targets[0]
    if pet_from is None or pet_to is None:
        return
    if get_debug_mode():
        print("transferring stats from :" + str(pet_from) + " to: " + str(pet_to))
    if copy_attack:
        pet_to.set_attack(pet_from.get_attack())
    if copy_health:
        pet_to.set_health(pet_from.get_health())


# dictionaries to  link target types with corresponding functions
targeting_functions = {
    None: lambda: [],
    TARGET.NA: lambda: [],
    TARGET.AdjacentAnimals: target_adjacent_animals,
    TARGET.All: target_all,
    TARGET.DifferentTierAnimals: target_different_tier_animals,
    TARGET.EachFriend: target_each_friend,
    # TARGET.EachShopAnimal: PetAbility.target_each_shop_animal(),
    TARGET.FirstEnemy: target_first_enemy,
    TARGET.FriendAhead: target_friend_ahead,
    TARGET.FriendBehind: target_friend_behind,
    TARGET.HighestHealthEnemy: target_highest_health_enemy,
    TARGET.LastEnemy: target_last_enemy,
    TARGET.LeftMostFriend: target_left_most_friend,
    TARGET.Level2And3Friends: target_level_2_and_3_friends,
    TARGET.LowestHealthEnemy: target_lowest_health_enemy,
    TARGET.RandomEnemy: target_random_enemy,
    TARGET.RandomFriend: target_random_friend,
    TARGET.RightMostFriend: target_right_most_friend,
    TARGET.Self: target_self,
    TARGET.StrongestFriend: target_strongest_friend,
    TARGET.TriggeringEntity: target_triggering_entity,
    TARGET.EachEnemy: target_each_enemy,
}

effect_functions = {
    None: lambda: None,
    EFFECT_TYPE.NA: None,
    EFFECT_TYPE.AllOf: all_of,
    EFFECT_TYPE.ApplyStatus: apply_status,
    EFFECT_TYPE.DealDamage: deal_damage,
    # EFFECT_TYPE.FoodMultiplier: food_multiplier,
    # EFFECT_TYPE.GainExperience: gain_experience,
    # EFFECT_TYPE.GainGold: gain_gold,
    EFFECT_TYPE.ModifyStats: modify_stats,
    EFFECT_TYPE.OneOf: one_of,
    EFFECT_TYPE.ReduceHealth: reduce_health,
    # EFFECT_TYPE.RefillShops: refill_shops,
    EFFECT_TYPE.RepeatAbility: repeat_ability,
    EFFECT_TYPE.SummonPet: summon_pet,
    EFFECT_TYPE.SummonRandomPet: summon_random_pet,
    EFFECT_TYPE.Swallow: swallow,
    # EFFECT_TYPE.TransferAbility: transfer_ability,
    EFFECT_TYPE.TransferStats: transfer_stats,
    EFFECT_TYPE.Evolve: evolve,
}


@total_ordering
class PetAbility:

    def __init__(self, pet, ability_data=None):

        # Initialize default ability
        self.pet = pet
        self.ability_data = ability_data
        self.name = self.pet.get_name_tag()
        self.level = self.pet.get_level()
        self.triggering_entity = None
        self.priority = 1
        self.is_targeted_ability = False
        self.perform_while_fainted = False
        self.targets = []
        self.effect = None
        self.effect_type = None
        self.target_info = None
        self.trigger = TRIGGER.NA
        self.triggered_by = TRIGGERED_BY.NA
        self.summon_random = False
        self.max_charges = None
        self.charges = 0

        # try to get effect
        try:
            self.effect = ability_data.get("effect")
        except AttributeError:
            pass

        # try to implement effect_type
        try:
            self.effect_type = EFFECT_TYPE[self.effect.get("kind")]
        except AttributeError:
            pass

        # try to implement target_info
        try:
            self.target_info = self.effect.get("target")
            self.is_targeted_ability = True
        except KeyError:
            pass
        except AttributeError:
            pass

        # try to implement trigger
        try:
            self.trigger = TRIGGER[self.ability_data.get("trigger")]
        except KeyError:
            pass
        except AttributeError:
            pass

        # try to implement triggered_by
        try:
            self.triggered_by = TRIGGERED_BY[self.ability_data.get("triggeredBy").get("kind")]
        except KeyError:
            pass
        except AttributeError:
            pass

        # try to implement triggered_by
        try:
            self.max_charges = self.ability_data.get("maxTriggers")
        except KeyError:
            pass
        except AttributeError:
            pass

        self.charges = self.max_charges

        if self.trigger == TRIGGER.Faint and self.triggered_by == TRIGGERED_BY.Self:
            self.perform_while_fainted = True

        # print(str(self.pet) + " | " + str(self.trigger) + " | " + str(self.triggered_by))

    def execute(self):

        if self.pet is None or self.pet.get_location() is None:
            return

        # if animal is fainted, then check if it can perform ability
        if self.pet.get_is_fainted():
            if not (self.triggered_by == TRIGGERED_BY.Self and self.trigger == TRIGGER.Faint):
                return

        # generate targets
        self.generate_targets()

        if get_debug_mode():
            print(self.pet.get_name() + " performs ability " + str(self.effect_type)[12:] + " to " + str(self.targets))

        # performs the function
        if self.charges is not None:
            if self.charges <= 0:
                return
            self.charges = self.charges - 1

        effect_functions[self.effect_type](self)

    def receive_trigger(self, trigger, triggering_entity):
        if trigger[0] == self.get_trigger() and trigger[1] == self.get_triggered_by():
            self.triggering_entity = triggering_entity
            if self.get_pet().get_location().is_battleground():
                self.get_pet().get_location().get_AM().send_triggers(TRIGGER.CastsAbility, self.get_pet())
            self.get_pet().get_location().get_AM().add_to_queue(self)

    # updates the list of targets for the ability when it is triggered, based on the target info

    def generate_targets(self):
        try:
            self.target_info = self.effect.get("target")
        except AttributeError:
            self.targets = []
            return

        # if no target info, return a blank list
        if self.target_info is None:
            self.targets = []
            return

        targeting_functions[TARGET[self.target_info.get("kind")]](self)

        # if ability is targeted check if targets exist, and remove any None targets
        if self.is_targeted_ability:
            if self.targets is None or all(x is None for x in self.targets):
                return
            self.targets = [x for x in self.targets if x is not None]

    def __eq__(self, other):
        return self.priority == other.priority and self.pet.get_attack() == other.pet.get_attack()

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.pet.get_attack() < other.pet.get_attack()
        else:
            return self.priority > other.priority

    def reset_max_triggers(self):
        self.charges = self.max_charges

    # getters and setters
    def get_trigger(self):
        return self.trigger

    def get_triggered_by(self):
        return self.triggered_by

    def get_pet(self):
        return self.pet

    def set_pet(self, pet):
        self.pet = pet

    def set_priority(self, prio):
        self.priority = prio

    def deep_copy(self):
        return copy.copy(self)

    def __str__(self):
        return str(self.pet) + " " + str(self.effect_type)  # + " " + str(self.trigger)
