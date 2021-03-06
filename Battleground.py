import random
from SuperAiPets import display_battle
from AbilityManager import *
from SAP_Data import get_game_speed, get_debug_mode, sfx_on

pygame.mixer.init()
smack = pygame.mixer.Sound("audio/sfx/smack.wav")

# ANIMATION TYPES : {required info}

# Attack : {} (makes the front two pets attack each other)
# ModifyStats/TransferStats/TransferAbility : {stats: STATS,
# from: INDEX, to: INDEX} (sends a burger then performs the action)
# DealDamage/Swallow : {damage: DAMAGE,
# from: INDEX, to: INDEX} (sends a rock and performs the action)
# ApplyStatus : {status: STATUS, from: INDEX,
# to: INDEX}
# Summon : {pet_to_summon: PET_OBJECT, index: INDEX} (usually preceded by a MovePets)
# Faint : {index_of: INDEX}
# MovePets : {[0,0,0,0,0,0,0,0,0,0]} (a list of 10 integers that represent the change in position for each of
# the pets) AllOf : A list of animation types to perform all at once

battle_bgs = [None] * 12
for i in range(0, 12):
    battle_bgs[i] = pygame.image.load(os.path.join("images/battle_screen/battle_bg_" + str(i) + ".png")).convert()


class Battleground:

    def __init__(self, team1, team2):

        self.team1 = team1.deep_copy()
        self.team2 = team2.deep_copy()
        self.team1.set_location(self)
        self.team2.set_location(self)
        self.battle_history = []
        # 0=in progress, 1=team1, 2=team2, 3=draw
        self.winner = 0
        self.left_bg = battle_bgs[0]
        self.right_bg = battle_bgs[1]

        self.AM = AbilityManager(self)

    def display(self):
        display_battle(self)

    def smack(self):

        if self.team1.get_pets()[4] is None or self.team2.get_pets()[4] is None:
            return

        team1_fighter = self.team1.pets[4]
        team2_fighter = self.team2.pets[4]

        if get_debug_mode():
            print(str(team1_fighter) + " | HP: " + str(team1_fighter.get_health()) + " | Attack: " + str(
                team1_fighter.get_attack()) + " | Status: " + str(team1_fighter.get_status())[7:])
            print(str(team2_fighter) + " | HP: " + str(team2_fighter.get_health()) + " | Attack: " + str(
                team2_fighter.get_attack()) + " | Status: " + str(team2_fighter.get_status())[7:])

        self.get_AM().send_triggers(TRIGGER.BeforeAttack, team1_fighter)
        self.get_AM().send_triggers(TRIGGER.BeforeAttack, team2_fighter)
        self.AM.perform_abilities()

        self.team1.remove_fainted()
        self.team2.remove_fainted()

        if self.team1.get_pets()[4] is None or self.team2.get_pets()[4] is None:
            return

        if get_debug_mode():
            print("Attack!")

        team1_fighter.attack_enemy(team2_fighter)
        team2_fighter.attack_enemy(team1_fighter)
        if sfx_on():
            pygame.mixer.Sound.play(smack)

        self.get_AM().send_triggers(TRIGGER.AfterAttack, team1_fighter)
        self.get_AM().send_triggers(TRIGGER.AfterAttack, team2_fighter)

        display_battle(self)

        time.sleep(get_game_speed())

        self.AM.perform_abilities()

        self.team1.remove_fainted()
        self.team2.remove_fainted()

    def battle(self):

        self.set_location()

        display_battle(self)
        self.get_AM().send_triggers(TRIGGER.StartOfBattle, None)
        self.AM.perform_abilities()

        display_battle(self)

        while self.team1.has_units() and self.team2.has_units():

            # move teams up to the front
            for k in range(4):
                self.team1.advance_team()
                self.team2.advance_team()

            display_battle(self)

            time.sleep(get_game_speed())

            self.smack()

            display_battle(self)

            time.sleep(get_game_speed())

            display_battle(self)

        display_battle(self)

        if self.team1.has_units():
            self.winner = 1
        elif self.team2.has_units():
            self.winner = 2
        else:
            self.winner = 3

        # time.sleep(2)

    def set_location(self):
        self.team1.set_location(self)
        self.team2.set_location(self)

    def is_battleground(self):
        return True

    def is_shop(self):
        return False

    def get_AM(self):
        return self.AM

    def set_team1(self, team1):
        self.team1 = team1

    def set_team2(self, team2):
        self.team2 = team2

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_enemy_team(self, team):
        teams = [self.team1, self.team2]
        teams.remove(team)
        return teams[0]

    def get_winner(self):
        return self.winner

    def reset_winner(self):
        self.winner = 0

    def get_all_pets(self):
        all_pets = []
        for j in range(5):
            all_pets.append(self.team1.get_pets()[j])
        for j in range(5):
            all_pets.append(self.team2.get_pets()[4 - j])
        return all_pets

    def randomize_battle_bgs(self):
        rando = random.sample(range(12), 2)
        self.left_bg = battle_bgs[rando[0]]
        self.right_bg = battle_bgs[rando[1]]
