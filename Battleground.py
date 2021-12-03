import copy
import pygame
from SuperAiPets import *
from AbilityManager import *


class Battleground:

    def __init__(self, team1, team2):
        self.team1 = []
        self.team2 = []
        # self.battleground = [None] * 10
        self.AM = AbilityManager()
        for i in range(5):
            self.team1.append(copy.copy(team1.get_pets()[i]))
            self.team1[i].set_battleground(self)
            self.team1[i].set_battleground_team(self.team1)
            self.team1[i].set_battleground_enemy_team(self.team2)
            self.team1[i].generate_ability()
            self.team2.append(copy.copy(team2.get_pets()[i]))
            self.team2[i].set_battleground(self)
            self.team2[i].set_battleground_team(self.team2)
            self.team2[i].set_battleground_enemy_team(self.team1)
            self.team2[i].generate_ability()

    def advance_team(self, team_number):
        if team_number == 1:
            team = self.team1
        elif team_number == 2:
            team = self.team2
        else:
            print("Index out of bounds for func advance_team_1")
            return
        for j in range(4):
            if team[4 - j] is None:
                team[4 - j] = team[3 - j]
                team[3 - j] = None
                # print("move " + str(3-j) + " to " + str(4-j))

    def smack(self):

        if self.team1[4] is None:
            print("Error, no fighter for team 1")
            return

        while self.team2[4] is None:
            print("Error, no fighter for team 1")
            return

        team1_fighter = self.team1[4]
        team2_fighter = self.team2[4]

        print(team1_fighter)
        print(team2_fighter)

        team1_fighter.take_damage(team2_fighter)
        team2_fighter.take_damage(team1_fighter)

        print(team1_fighter)
        print(team2_fighter)

        self.AM.perform_abilities()

        for x in self.team1:
            if x is not None and x.get_is_fainted():
                self.team1[self.team1.index(x)] = None

        for x in self.team2:
            if x is not None and x.get_is_fainted():
                self.team2[self.team2.index(x)] = None

    def battle(self):

        display_battle(self)
        # time.sleep(0.5)

        for k in range(4):
            self.advance_team(1)
            self.advance_team(2)

        team1_has_units = (self.team1[4] is not None)
        team2_has_units = (self.team2[4] is not None)

        while team1_has_units and team2_has_units:

            # move teams up to the front
            while self.team1[4] is None:
                self.advance_team(1)

            while self.team2[4] is None:
                self.advance_team(2)

            print("fighting")
            self.smack()

            display_battle(self)
            # time.sleep(0.5)

            team1_has_units = False
            team2_has_units = False

            for x in self.team1:
                if x is not None:
                    team1_has_units = True
                    break

            for x in self.team2:
                if x is not None:
                    team2_has_units = True
                    break

        display_battle(self)
        # time.sleep(0.5)

        # print(self.battleground[4])

        # for k in range(4):
        #     self.advance_team(1)
        #     self.advance_team(2)

        # print(battleground)
        # print("cock and ball torture")
        # display_battle(self)
        # time.sleep(0.5)

        if team1_has_units:
            # winner = team1
            print("team 1 wins")

        if team2_has_units:
            # winner = team2
            print("team 2 wins")

        # time.sleep(2)

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2
