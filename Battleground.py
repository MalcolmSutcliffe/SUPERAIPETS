import copy
import time

import pygame
from SuperAiPets import *
from AbilityManager import *
from SAP_Data import get_game_speed, get_debug_mode

# ANIMATION TYPES : {required info}

# Attack : {} (makes the front two pets attack each other)
# ModifyStats/TransferStats/TransferAbility : {stats: STATS, from: INDEX, to: INDEX} (sends a burger then performs the action)
# DealDamage/Swallow : {damage: DAMAGE, from: INDEX, to: INDEX} (sends a rock and performs the action)
# ApplyStatus : {status: STATUS, from: INDEX, to: INDEX}
# Summon : {pet_to_summon: PET_OBJECT, index: INDEX} (usually preceded by a MovePets)
# Faint : {index_of: INDEX}
# MovePets : {[0,0,0,0,0,0,0,0,0,0]} (a list of 10 integers that represent the change in position for each of the pets)
# AllOf : A list of animation types to perform all at once


class Battleground:

    def __init__(self, team1, team2):

        self.team1 = copy.copy(team1)
        self.team2 = copy.copy(team2)
        self.team1.set_battleground(self)
        self.team2.set_battleground(self)
        self.battle_history = []
        #0=in progress, 1=team1, 2=team2, 3=draw
        self.winner = 0

        self.AM = AbilityManager(self)

        for i in range(5):

            self.team1.pets[i] = copy.copy(team1.get_pets()[i])
            if self.team1.pets[i] is not None:
                self.team1.pets[i].set_battleground(self)
                self.team1.pets[i].set_battleground_team(self.team1)
                self.team1.pets[i].set_battleground_enemy_team(self.team2)
                self.team1.pets[i].generate_ability()

            self.team2.pets[i] = copy.copy(team2.get_pets()[i])
            if self.team2.pets[i] is not None:
                self.team2.pets[i].set_battleground(self)
                self.team2.pets[i].set_battleground_team(self.team2)
                self.team2.pets[i].set_battleground_enemy_team(self.team1)
                self.team2.pets[i].generate_ability()

    def display(self):
        display_battle(self)

    def smack(self):

        if self.team1.get_pets()[4] is None or self.team2.get_pets()[4] is None:
            return

        team1_fighter = self.team1.pets[4]
        team2_fighter = self.team2.pets[4]

        if get_debug_mode():
            print(str(team1_fighter) + " | HP: " + str(team1_fighter.get_health()) + " | Attack: " + str(
                team1_fighter.get_attack()))
            print(str(team2_fighter) + " | HP: " + str(team2_fighter.get_health()) + " | Attack: " + str(
                team2_fighter.get_attack()))

        send_triggers(TRIGGER.BeforeAttack, team1_fighter, self)
        send_triggers(TRIGGER.BeforeAttack, team2_fighter, self)
        self.AM.perform_abilities()

        self.team1.remove_fainted()
        self.team2.remove_fainted()

        if self.team1.get_pets()[4] is None or self.team2.get_pets()[4] is None:
            return

        if get_debug_mode():
            print("Attack!")

        team1_fighter.attack_enemy(team2_fighter)
        team2_fighter.attack_enemy(team1_fighter)

        send_triggers(TRIGGER.AfterAttack, team1_fighter, self)
        send_triggers(TRIGGER.AfterAttack, team2_fighter, self)

        display_battle(self)

        time.sleep(get_game_speed())

        self.AM.perform_abilities()

        self.team1.remove_fainted()

        self.team2.remove_fainted()

    def battle(self):

        GAME_SPEED = get_game_speed()

        display_battle(self)
        # time.sleep(GAME_SPEED)
        send_triggers(TRIGGER.StartOfBattle, None, self)
        self.AM.perform_abilities()

        display_battle(self)

        while self.team1.has_units() and self.team2.has_units():

            # move teams up to the front
            for k in range(4):
                self.team1.advance_team()
                self.team2.advance_team()

            display_battle(self)

            time.sleep(GAME_SPEED)

            self.smack()

            display_battle(self)
            time.sleep(GAME_SPEED)

            display_battle(self)
            # time.sleep(GAME_SPEED)

        display_battle(self)
        # time.sleep(GAME_SPEED)

        # print(self.battleground[4])

        # for k in range(4):
        #     self.advance_team(1)
        #     self.advance_team(2)

        # print(battleground)
        # print("cock and ball torture")
        # display_battle(self)
        # time.sleep(GAME_SPEED)

        if self.team1.has_units():
            self.winner = 1
        elif self.team2.has_units():
            self.winner = 2
        else:
            self.winner = 3

        # time.sleep(2)

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_winner(self):
        return self.winner

    def get_all_pets(self):
        all_pets = []
        for i in range(5):
            all_pets.append(self.team1.get_pets()[i])
        for i in range(5):
            all_pets.append(self.team2.get_pets()[4 - i])
        return all_pets
