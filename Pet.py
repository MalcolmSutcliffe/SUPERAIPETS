from PetAbility import PetAbility
from AbilityManager import *
from SAP_Data import DATA, default_texture
from Status import STATUS
import os


class Pet:

    def __init__(self, name_tag="", team=None, battleground=None, status=None):

        self.base_attack = 0
        self.base_health = 0

        self.level = 1

        self.is_fainted = False

        self.status = status

        self.team = team
        self.battleground = battleground
        self.battleground_team = None
        self.battleground_enemy_team = None

        self.name = name_tag
        self.name_tag = "pet-" + name_tag
        pet_data = DATA.get("pets").get("bee")

        try:
            pet_data = DATA.get("pets").get(self.name_tag)
        except AttributeError:
            print("Error: the pet tag '" + self.name_tag + "' does not exist!")

        try:
            self.base_attack = pet_data.get("baseAttack")
            self.base_health = pet_data.get("baseHealth")
            self.packs = pet_data.get("packs")
            self.tier = pet_data.get("tier")
            self.ability = PetAbility(self)
        except AttributeError:
            self.ability = None

        self.temp_attack = 0
        self.temp_health = 0
        self.attack = self.base_attack
        self.health = self.base_health
        self.experience = 0
        self.status = None
        try:
            self.rightSprite = pygame.transform.scale(
                pygame.image.load(os.path.join('images/pet-images', self.name_tag + ".png")), (128, 128))
        except FileNotFoundError:
            self.rightSprite = default_texture
            print("image for '" + name_tag + "' not found")
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

    def receive_trigger(self, trigger, triggering_entity):
        if self.ability is None:
            return
        if trigger[0] == self.ability.get_trigger() and trigger[1] == self.ability.get_triggered_by():
            self.ability.triggering_entity = triggering_entity
            self.battleground.AM.add_to_queue(self.ability)

    def get_dmg(self):

        dmg = self.attack

        if self.status == STATUS.STEAK_ATTACK:
            dmg += 20
            self.status = None

        if self.status == STATUS.BONE_ATTACK:
            dmg += 5

        return dmg

    def attack_enemy(self, victim):

        victim.take_damage(self, self.get_dmg())

        if self.status == STATUS.SPLASH_ATTACK:
            for i in range(4):
                x = victim.get_battleground_team().get_pets()[3-i]
                if x is not None:
                    x.take_damage(self, 5)
                    break

    def take_damage(self, attacker, dmg):

        if self.status == STATUS.WEAK:
            dmg += 3

        if self.status == STATUS.GARLIC_ARMOR:
            dmg -= 2
            if dmg < 2:
                dmg = 1

        if self.status == STATUS.MELON_ARMOR:
            dmg -= 20
            if dmg < 0:
                dmg = 0
            self.status = None

        if self.status == STATUS.COCONUT_SHIELD:
            dmg = 0
            self.status = None

        self.health = self.health - dmg

        if self.health <= 0 and not self.is_fainted:
            self.faint()
            send_triggers(TRIGGER.KnockOut, attacker, self.battleground)

        send_triggers(TRIGGER.Hurt, self, self.battleground)

    def faint(self):
        if self.battleground is not None:
            send_triggers(TRIGGER.Faint, self, self.battleground)
        else:
            pass
        # self.battleground_team[self.battleground_team.index(self)] = None
        print(self.name + " has fainted!")
        self.is_fainted = True

        team = self.battleground_team
        if team is None:
            team = self.team

        if self.status == STATUS.HONEY_BEE:
            team.summon_pet(self.get_index(), "bee", 1, 1, None)

        if self.status == STATUS.EXTRA_LIFE:
            team.summon_pet(self.get_index(), self.name, 1, 1, None)

    def die(self):
        self.end_of_battle()
        del self

    def end_of_battle(self):
        self.battleground_team.get_pets()[self.battleground_team.get_pets().index(self)] = None
        self.battleground_team = None
        self.battleground_enemy_team = None
        self.battleground = None

    def gain_stats(self, stats, stat_type=0):  # (0 = permanent stats, #1 = temp stat)
        if stat_type == 0:
            self.base_attack += stats[0]
            self.base_health += stats[1]
        if stat_type == 1:
            self.temp_attack += stats[0]
            self.temp_health += stats[1]
        self.attack += stats[0]
        self.health += stats[1]
        print(str(self) + " gained " + str(stats[0]) + " attack and " + str(stats[1]) + " health.")

    def gain_exp(self, exp):
        self.experience += exp
        if 2 <= self.experience < 6:
            self.level = 2
        elif 6 <= self.experience:
            self.level = 3

    def generate_ability(self):
        self.ability = PetAbility(self)

    # getters and setters
    def get_name_tag(self):
        return self.name_tag

    def get_sprite(self, direction):
        if direction == 0:
            return self.leftSprite
        elif direction == 1:
            return self.rightSprite
        else:
            return default_texture

    def get_attack(self):
        return self.attack

    def get_health(self):
        return self.health

    def get_battleground(self):
        return self.battleground

    def get_team(self):
        return self.team

    def get_battleground_team(self):
        return self.battleground_team

    def get_battleground_enemy_team(self):
        return self.battleground_enemy_team

    def get_base_attack(self):
        return self.base_attack

    def get_base_health(self):
        return self.base_health

    def get_temp_attack(self):
        return self.temp_attack

    def get_temp_health(self):
        return self.temp_attack

    def get_level(self):
        return self.level

    def get_tier(self):
        return self.tier

    def get_is_fainted(self):
        return self.is_fainted

    def get_status(self):
        return self.status

    def get_index(self):
        team = self.battleground_team
        if team is None:
            team = self.team
        return team.get_pets().index(self)

    def set_team(self, team):
        self.team = team

    def set_battleground(self, bg):
        self.battleground = bg

    def set_battleground_team(self, bg_team):
        self.battleground_team = bg_team

    def set_battleground_enemy_team(self, bg_en_team):
        self.battleground_enemy_team = bg_en_team

    def set_base_attack(self, ba):
        self.base_attack = ba
        self.attack = self.base_attack + self.temp_attack

    def set_base_health(self, bh):
        self.base_health = bh
        self.health = self.base_health + self.temp_health

    def set_temp_attack(self, ta):
        self.temp_attack = ta

    def set_temp_health(self, th):
        self.temp_health = th

    def set_status(self, status):
        self.status = status

    def set_level(self, lvl):
        self.level = lvl

    def __str__(self):
        return self.name
