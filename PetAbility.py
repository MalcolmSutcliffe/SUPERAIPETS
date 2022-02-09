import copy
import random
from functools import total_ordering
from AbilityManager import *
from SAP_Data import *


@total_ordering
class PetAbility:

    def __init__(self, pet, ability_data=None):

        self.pet = pet
        self.ability_data = ability_data
        self.name = self.pet.get_name_tag()
        self.level = self.pet.get_level()
        self.triggering_entity = None
        self.priority = 1
        self.effect_type = None

        if self.ability_data is None:
            try:
                self.ability_data = PET_DATA.get(self.name).get("level" + str(self.level) + "Ability")
            except AttributeError:
                print("Error: the pet tag '" + self.name + "' does not exist!")
            try:
                self.description = self.ability_data.get("description")
                self.trigger = TRIGGER[self.ability_data.get("trigger")]
                self.triggered_by = TRIGGERED_BY[self.ability_data.get("triggeredBy").get("kind")]
                self.effect = self.ability_data.get("effect")
                self.effect_type = EFFECT_TYPE[self.effect.get("kind")]
            except AttributeError:
                self.description = DEFAULT_ABILITY.get("description")
                self.trigger = TRIGGER[DEFAULT_ABILITY.get("trigger")]
                self.triggered_by = TRIGGERED_BY[DEFAULT_ABILITY.get("triggeredBy").get("kind")]
                self.effect = DEFAULT_ABILITY.get("effect")

        else:
            self.effect = ability_data
            self.effect_type = EFFECT_TYPE[self.ability_data.get("kind")]

    def execute(self):

        if self.pet is None or self.pet.get_battleground() is None:
            return

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

        # RepeatAbility
        if self.effect_type == EFFECT_TYPE.RepeatAbility:
            self.repeat_ability(self.triggering_entity)
            return

        if get_debug_mode():
            print(str(self.pet) + " used their " + str(self.effect_type) + " ability!")

        # SummonPet
        if self.effect_type == EFFECT_TYPE.SummonPet:
            if self.pet.name == "fly" and (self.triggering_entity.name == "zombie-fly"):
                return
            self.summon(self.triggering_entity, False)
            return

        # SummonRandomPet
        if self.effect_type == EFFECT_TYPE.SummonRandomPet:
            self.summon(self.triggering_entity, True)
            return

        # Evolve
        if self.effect_type == EFFECT_TYPE.Evolve:
            self.evolve()
            return

        # TransferStats
        if self.effect_type == EFFECT_TYPE.TransferStats:
            self.transfer_stats()
            return

        # targeted abilities
        targets = self.generate_targets(self.effect.get("target"))

        if targets is None or all(x is None for x in targets):
            return

        targets = [i for i in targets if i is not None]

        # ModifyStats
        if self.effect_type == EFFECT_TYPE.ModifyStats:
            for target in targets:
                self.modify_stats(target)
            return

        # DealDamage
        if self.effect_type == EFFECT_TYPE.DealDamage:
            for target in targets:
                if get_debug_mode():
                    print(str(self.pet) + " did damage to " + str(target))
                self.deal_damage(target)
            return

        # ApplyStatus
        if self.effect_type == EFFECT_TYPE.ApplyStatus:
            for target in targets:
                self.apply_status(target)
            return

        # ReduceHealth
        if self.effect_type == EFFECT_TYPE.ReduceHealth:
            for target in targets:
                self.reduce_health(target)

        # Swallow
        if self.effect_type == EFFECT_TYPE.Swallow:
            for target in targets:
                self.swallow(target)

    # generates the list of targets for the ability when it is triggered, based on the passed target info
    def generate_targets(self, target_info):

        if target_info is None:
            return
        try:
            team = copy.copy(self.pet.get_battleground_team().get_pets())
        except AttributeError:
            return

        if team is None:
            team = copy.copy(self.pet.get_team().get_pets())

        if team is None:
            return

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
            targets = copy.copy(team)
            targets = [x for x in targets if x is not None]
            targets = [x for x in targets if not x.get_is_fainted()]
            n = min(n, len(targets))
            targets = random.sample(targets, n)
            return targets

        # RandomEnemy
        if kind == TARGET.RandomEnemy:
            n = target_info.get("n")
            targets = copy.copy(enemy_team)
            targets = [x for x in targets if x is not None]
            targets = [x for x in targets if not x.get_is_fainted()]
            n = min(n, len(targets))
            targets = random.sample(targets, n)
            return targets

        # All
        if kind == TARGET.All:
            for x in team:
                if x is not None:
                    targets.append(x)
            if enemy_team is not None:
                for x in enemy_team:
                    if x is not None:
                        targets.append(x)
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

        # EachFriend
        if kind == TARGET.EachEnemy:
            return enemy_team

        # EachShopAnimal
        if kind == TARGET.EachShopAnimal:
            return None
            # not implemented

        # FirstEnemy
        if kind == TARGET.FirstEnemy:
            targets = [j for j in enemy_team if j is not None and not j.get_is_fainted()]
            if len(targets) > 0:
                return [targets[len(targets) - 1]]
            return

        # FriendAhead
        if kind == TARGET.FriendAhead:
            n = target_info.get("n")
            team = [j for j in team if j is not None]
            team = [j for j in team if not j.get_is_fainted()]
            for k in range(n):
                for j in range(team.index(self.pet) + 1, 5):
                    if j < len(team) and team[j] is not None and targets.count(team[j]) == 0:
                        targets.append(team[j])
                        break
            return targets

        # FriendBehind
        if kind == TARGET.FriendBehind:
            n = target_info.get("n")
            for k in range(n):
                index = team.index(self.pet)
                for j in range(1, index):
                    if index - j >= 0 and team[index - j] is not None and targets.count(team[index - j]) == 0:
                        targets.append(team[index - j])
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
                if x is not None and not x.get_is_fainted():
                    targets.append(x)
                    return targets

        # LeftMostFriend
        if kind == TARGET.LeftMostFriend:
            for k in range(5):
                if team[k] is not None:
                    targets.append(team[k])
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
                elif x is not None and x.get_health() < target.get_health() and not x.get_is_fainted():
                    target = x
            targets.append(target)
            return targets

        # RightMostFriend
        if kind == TARGET.RightMostFriend:
            for k in range(5):
                if team[4 - k] is not None:
                    targets.append(team[4 - k])
                    return targets

        # StrongestFriend
        if kind == TARGET.StrongestFriend:
            target = None
            for x in team:
                if target is None:
                    target = x
                elif x is not None and x.get_health() + x.get_attack() > target.get_health() + target.get_attack():
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

        if stats[0] == "this":
            stats[0] = self.pet.get_attack()

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

        if summon_attack != "this":
            pass
        else:
            summon_attack = self.pet.get_attack()

        if summon_attack is None:
            summon_attack = PET_DATA.get("pet-" + summon_tag).get("baseAttack")
        if summon_health is None:
            summon_health = PET_DATA.get("pet-" + summon_tag).get("baseHealth")

        try:
            status = STATUS[self.effect.get("withStatus")]
        except KeyError:
            status = None

        level = self.effect.get("withLevel")

        if level is None:
            level = 1

        team = self.pet.get_battleground_team()
        if team is None:
            team = self.pet.get_team()

        if team is None:
            return

        try:
            target_index = team.get_pets().index(target)
        except ValueError:
            target_index = 4

        if summon_team == "Enemy":
            team = self.pet.get_battleground_enemy_team()
            target_index = 0

        if team is None:
            return

        if n is None:
            n = 1

        for i in range(n):
            team.summon_pet(target_index, summon_tag, summon_attack, summon_health, level, status)

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

    def repeat_ability(self, target):
        n = self.effect.get("n")
        for i in range(n):
            target.get_battleground().AM.add_to_queue(target.get_ability())

    def reduce_health(self, target):
        percent = self.effect.get("percentage")
        if get_debug_mode():
            print(str(self.pet) + " reduced " + str(target) + "'s health by " + str(percent * 100) + "%")
        new_health = int(target.get_health() * (1 - percent))
        if new_health <= 0:
            new_health = 1
        target.set_health(new_health)

    def swallow(self, target):
        self.trigger = TRIGGER.Faint
        self.triggered_by = TRIGGERED_BY.Self
        self.effect_type = EFFECT_TYPE.SummonPet
        self.effect = \
            {"kind": "SummonPet",
             "pet": target.get_name_tag(),
             "team": "Friendly",
             "withHealh": 1,
             "withAttack": 1,
             "withLevel": self.level}
        target.faint()

    def evolve(self):

        summon_attack = self.effect.get("withAttack")
        summon_health = self.effect.get("withHealth")
        status = None
        level = 1

        summon_tag = self.effect.get("into")
        summon_tag = summon_tag[4:]

        if summon_attack == "this":
            summon_attack = self.pet.get_attack()

        if summon_attack is None:
            summon_attack = PET_DATA.get("pet-" + summon_tag).get("baseAttack")
        if summon_health is None:
            summon_health = PET_DATA.get("pet-" + summon_tag).get("baseHealth")

        team = self.pet.get_battleground_team()
        if team is None:
            team = self.pet.get_team()

        if team is None:
            return
        try:
            target_index = team.get_pets().index(self.pet)
        except ValueError:
            target_index = 4

        self.pet.faint()

        team.summon_pet(target_index, summon_tag, summon_attack, summon_health, level, None)

    def transfer_stats(self):
        copy_attack = self.effect.get("copyAttack")
        copy_health = self.effect.get("copyHealth")
        pet_from = self.generate_targets(self.effect.get("from"))[0]
        pet_to = self.generate_targets(self.effect.get("to"))[0]
        if pet_from is None or pet_to is None:
            return
        if get_debug_mode():
            print("transfering stats from :" + str(pet_from) + " to: " + str(pet_to))
        if copy_attack:
            pet_to.set_attack(pet_from.get_attack())
        if copy_health:
            pet_to.set_health(pet_from.get_health())
        # "effect": {
        #     "kind": "TransferStats",
        #     "copyAttack": true,
        #     "copyHealth": true,
        #     "from": {
        #         "kind": "StrongestFriend"
        #     },
        #     "to": {
        #         "kind": "Self"
        #     }

    def __eq__(self, other):
        return self.priority == other.priority and self.pet.get_attack() == other.pet.get_attack()

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.pet.get_attack() < other.pet.get_attack()
        else:
            return self.priority > other.priority

    # getters and setters
    def get_trigger(self):
        return self.trigger

    def get_triggered_by(self):
        return self.triggered_by

    def set_priority(self, prio):
        self.priority = prio

    def __str__(self):
        return str(self.pet) + " " + str(self.effect_type)  # + " " + str(self.trigger)
