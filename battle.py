import pygame
import time
from SuperAiPets import display_battle
from Team import Team
from Pet import Pet


def create_battleground(team1, team2):
    # initialize the battleground
    battleground = [None] * 10
    for i in range(5):
        battleground[i] = team1.get_pets()[i]
        battleground[i + 5] = team2.get_pets()[4-i]
    return battleground


def move_teams_up_one(battleground):
    # team1
    for j in range(4):
        if battleground[4 - j] is None:
            battleground[4 - j] = battleground[3 - j]
            battleground[3 - j] = None
            # print("move " + str(3-j) + " to " + str(4-j))

    # team2
    for j in range(5, 9):
        if battleground[j] is None:
            battleground[j] = battleground[j + 1]
            battleground[j + 1] = None

    return battleground


def fight(battleground):
    display_battle(battleground)
    # time.sleep(0.5)

    battleground = move_teams_up_one(battleground)
    display_battle(battleground)

    team1_fighter = battleground[4]
    team2_fighter = battleground[5]
    # add abilities tagged as "before attack" for units 4,5 to queue
    # perform abilities
    print("team 1 hp: " + str(team1_fighter.get_health()))
    print("team 2 hp: " + str(team2_fighter.get_health()))

    print("team 1 attacks for: " + str(team1_fighter.get_attack()) + " damage")
    print("team 2 attacks for: " + str(team2_fighter.get_attack()) + " damage")

    team1_fighter.take_damage(team2_fighter.get_attack())
    team2_fighter.take_damage(team1_fighter.get_attack())

    print("team 1 hp: " + str(team1_fighter.get_health()))
    print("team 2 hp: " + str(team2_fighter.get_health()))
    # add abilities tagged as "on unit in front take damage" for units 3 and 6 to queue
    if team1_fighter.get_health() <= 0:
        battleground[4] = None
        # add abilities tagged as "on faint" for unit 4 to queue
        # add abilities tagged as "on unit in front faint" for units 3 to queue
        # add abilities tagged as "on friend faints" for units 0,1,2,3 to queue
        # print("team 1 animal died lol")
    if team2_fighter.get_health() <= 0:
        battleground[5] = None
        # add abilities tagged as "on faint" for unit 5 to queue
        # add abilities tagged as "on unit in front faint" for units 6 to queue
        # add abilities tagged as "on friend faints" for units 6,7,8,9 to queue
        # print("team 2 animal died lol")
    # perform abilities
    display_battle(battleground)
    # time.sleep(0.5)


def battle(team1, team2):
    battleground = create_battleground(team1, team2)

    display_battle(battleground)
    time.sleep(0.5)

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
