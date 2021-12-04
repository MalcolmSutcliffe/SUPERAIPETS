import copy
import time

import pygame
from SuperAiPets import *
from AbilityManager import *
from SAP_Data import GAME_SPEED


class Battleground:

    def __init__(self, team1, team2):

        self.team1 = copy.copy(team1)
        self.team2 = copy.copy(team2)
        self.team1.set_battleground(self)
        self.team2.set_battleground(self)

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

    def smack(self):

        display_battle(self)

        time.sleep(GAME_SPEED)

        if self.team1.pets[4] is None:
            print("Error, no fighter for team 1")
            return

        while self.team2.pets[4] is None:
            print("Error, no fighter for team 1")
            return

        team1_fighter = self.team1.pets[4]
        team2_fighter = self.team2.pets[4]

        print(str(team1_fighter) + " | HP: " + str(team1_fighter.get_health()) + " | Attack: " + str(
            team1_fighter.get_attack()))
        print(str(team2_fighter) + " | HP: " + str(team2_fighter.get_health()) + " | Attack: " + str(
            team2_fighter.get_attack()))

        send_triggers(TRIGGER.BeforeAttack, team1_fighter, self)
        send_triggers(TRIGGER.BeforeAttack, team2_fighter, self)

        team1_fighter.take_damage(team2_fighter, team2_fighter.get_dmg())
        team2_fighter.take_damage(team1_fighter, team1_fighter.get_dmg())

        send_triggers(TRIGGER.AfterAttack, team1_fighter, self)
        send_triggers(TRIGGER.AfterAttack, team2_fighter, self)

        print(str(team1_fighter) + " | HP: " + str(team1_fighter.get_health()) + " | Attack: " + str(
            team1_fighter.get_attack()))
        print(str(team2_fighter) + " | HP: " + str(team2_fighter.get_health()) + " | Attack: " + str(
            team2_fighter.get_attack()))

        self.AM.perform_abilities()

        self.team1.remove_fainted()

        self.team2.remove_fainted()

    def battle(self):

        display_battle(self)
        # time.sleep(GAME_SPEED)
        send_triggers(TRIGGER.StartOfBattle, None, self)

        for k in range(4):
            self.team1.advance_team()
            self.team2.advance_team()

        time.sleep(GAME_SPEED)

        while self.team1.has_units() and self.team2.has_units():

            # move teams up to the front
            while self.team1.pets[4] is None:
                self.team1.advance_team()

            while self.team2.pets[4] is None:
                self.team2.advance_team()

            time.sleep(GAME_SPEED)

            print("fighting")
            self.smack()

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
            # winner = team1
            print("team 1 wins")

        elif self.team2.has_units():
            # winner = team2
            print("team 2 wins")

        else:
            print("Draw")

        # time.sleep(2)

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_all_pets(self):
        all_pets = []
        for i in range(5):
            all_pets.append(self.team1.get_pets()[i])
        for i in range(5):
            all_pets.append(self.team2.get_pets()[4-i])
        return all_pets
