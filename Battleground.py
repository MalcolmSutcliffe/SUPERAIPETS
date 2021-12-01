import copy
import pygame
from SuperAiPets import *
from AbilityManager import *


class Battleground:

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.battleground = [None] * 10
        self.AM = AbilityManager()
        for i in range(5):
            self.battleground[i] = copy.copy(team1.get_pets()[i])
            self.battleground[i + 5] = copy.copy(team2.get_pets()[4 - i])

    def advance_team_1(self):
        # team1
        for j in range(4):
            if self.battleground[4 - j] is None:
                self.battleground[4 - j] = self.battleground[3 - j]
                self.battleground[3 - j] = None
                # print("move " + str(3-j) + " to " + str(4-j))

    def advance_team_2(self):
        # team2
        for j in range(5, 9):
            if self.battleground[j] is None:
                self.battleground[j] = self.battleground[j + 1]
                self.battleground[j + 1] = None

    def smack(self):

        while self.battleground[4] is None:
            self.advance_team_1()

        while self.battleground[5] is None:
            self.advance_team_2()

        team1_fighter = self.battleground[4]
        team2_fighter = self.battleground[5]

        print("team 1 hp: " + str(team1_fighter.get_health()))
        print("team 2 hp: " + str(team2_fighter.get_health()))

        print("team 1 attacks for: " + str(team1_fighter.get_attack()) + " damage")
        print("team 2 attacks for: " + str(team2_fighter.get_attack()) + " damage")

        team1_fighter.take_damage(team2_fighter.get_attack())
        team2_fighter.take_damage(team1_fighter.get_attack())

        print("team 1 hp: " + str(team1_fighter.get_health()))
        print("team 2 hp: " + str(team2_fighter.get_health()))

        if team1_fighter.get_health() <= 0:
            team1_fighter.faint()
            self.battleground[4] = None
            print("team 1 animal '" + team1_fighter.get_name_tag() + "' has fainted!")
        if team2_fighter.get_health() <= 0:
            team2_fighter.faint()
            self.battleground[5] = None
            print("team 2 animal '" + team2_fighter.get_name_tag() + "' has fainted!")

    def battle(self):

        display_battle(self)
        # time.sleep(0.5)

        for k in range(4):
            self.advance_team_1()
            self.advance_team_2()

        team1_has_units = (self.battleground[4] is not None)
        team2_has_units = (self.battleground[5] is not None)

        while team1_has_units and team2_has_units:
            # move teams up one spot if there is space
            self.advance_team_1()
            self.advance_team_2()

            print("fighting")
            self.smack()

            display_battle(self)
            # time.sleep(0.5)

            team1_has_units = False
            team2_has_units = False

            for i in range(5):
                if self.battleground[i] is not None:
                    team1_has_units = True
                if self.battleground[i + 5] is not None:
                    team2_has_units = True

        display_battle(self)
        # time.sleep(0.5)

        # print(self.battleground[4])

        for k in range(4):
            self.advance_team_1()
            self.advance_team_1()

        # print(battleground)
        # print("cock and ball torture")
        display_battle(self)
        # time.sleep(0.5)

        if team1_has_units:
            # winner = team1
            print("team 1 wins")

        if team2_has_units:
            # winner = team2
            print("team 2 wins")

        # time.sleep(2)
