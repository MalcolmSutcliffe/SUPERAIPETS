#import pygame
from Team import Team
from Pet import Pet


def main():
    team1 = Team()
    team2 = Team()
    myFish = Pet("Fish", 2, 3, 0, 0, 0)
    team1.add_pet()
    battle(team1, team2)


if __name__ == "__main__":
    main()


def battle(team1, team2):
    # initialize the battleground
    battleground = team1.pets | team2.pets.reverse()

    team1_has_units = False
    team2_has_units = False

    for i in range(5):
        if battleground[i] is not None:
            team1_has_units = True
        if battleground[i + 5] is not None:
            team2_has_units = True

    while team1_has_units & team2_has_units:

        # move teams up one spot if there is space
        def move_teams_up_one():
            # team1
            for i in range(4):
                if battleground[4 - i] is None:
                    battleground[4 - i] = battleground[3 - i]
                    battleground[3 - i] = None
            # team2
            for i in range(5, 9):
                if battleground[i] is None:
                    battleground[i] = battleground[i + 1]
                    battleground[i + 1] = None

        def fight():
            for i in range(4):
                move_teams_up_one()
            team1_fighter = battleground[4]
            team2_fighter = battleground[5]
            # add abilities tagged as "before attack" for units 4,5 to queue
            # perform abilities
            team1_fighter.take_damage(team2_fighter.get_damage())
            team2_fighter.take_damage(team1_fighter.get_damage())
            # add abilities tagged as "on unit infront take damage" for units 3 and 6 to queue
            if team1_fighter.get_health <= 0:
                battleground[4] = None
                # add abilities tagged as "on faint" for unit 4 to queue
                # add abilities tagged as "on unit infront faint" for units 3 to queue
                # add abilities tagged as "on friend faints" for units 0,1,2,3 to queue
            if team1_fighter.get_health <= 0:
                battleground[4] = None
                # add abilities tagged as "on faint" for unit 5 to queue
                # add abilities tagged as "on unit infront faint" for units 6 to queue
                # add abilities tagged as "on friend faints" for units 6,7,8,9 to queue
            # perform abilities

        fight()

        for i in range(5):
            if battleground[i] is not None:
                team1_has_units = True
            if battleground[i + 5] is not None:
                team2_has_units = True

        if team1_has_units:
            winner = team1

        if team2_has_units:
            winner = team2
