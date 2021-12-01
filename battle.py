import pygame
import time
from SuperAiPets import display_battle
from Battleground import Battleground
from Team import Team
from Pet import Pet


def battle(team1, team2):
    battleground = Battleground(team1, team2)

    display_battle(battleground)
    # time.sleep(0.5)

    for k in range(4):
        battleground = move_teams_up_one(battleground)

    team1_has_units = False
    team2_has_units = False

    for i in range(5):
        if battleground[i] is not None:
            team1_has_units = True
        if battleground[i + 5] is not None:
            team2_has_units = True

    while team1_has_units and team2_has_units:
        # move teams up one spot if there is space
        battleground = move_teams_up_one(battleground)

        print("fighting")
        fight(battleground)

        display_battle(battleground)
        # time.sleep(0.5)

        team1_has_units = False
        team2_has_units = False

        for i in range(5):
            if battleground[i] is not None:
                team1_has_units = True
            if battleground[i + 5] is not None:
                team2_has_units = True

    display_battle(battleground)
    # time.sleep(0.5)

    print(battleground[4])

    for k in range(4):
        move_teams_up_one(battleground)

    # print(battleground)
    # print("cock and ball torture")
    display_battle(battleground)
    # time.sleep(0.5)

    if team1_has_units:
        winner = team1
        print("team 1 wins")

    if team2_has_units:
        winner = team2
        print("team 2 wins")

    # time.sleep(2)
