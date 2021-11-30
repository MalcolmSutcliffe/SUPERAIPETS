import pygame
import os
from battle import *
from Team import Team
from Pet import Pet
import json

# initialize the pygame module
pygame.display.init()
pygame.font.init()
# load and set the logo
pygame.display.set_caption("SUPERAIPETS")

# create window
window = pygame.display.set_mode((1280, 720))
# fish_Texture = pygame.image.load(os.path.join('images', 'pet-fish.png'))
main_menu_bg = pygame.image.load(os.path.join('images', 'main_menu.png'))


def display_battle(battleground):
    pygame.display.flip()
    window.fill((0, 255, 0))
    i = 0
    for x in battleground:
        if x is not None:
            if i <= 4:
                window.blit(x.leftSprite, ((150 + (94 * i)), 300))
            else:
                window.blit(x.rightSprite, ((150 + (94 * i)), 300))
        i += 1
    i = 0


def main():

    # f = open("SAPinfo.json")
    # data = json.load(f)
    # f.close()
    # for i in data.get("pets"):
    #     print(i)
    # print(data.get("pets").get("pet-ant").get("level1Ability"))

    team1 = Team()
    team2 = Team()
    my_fishes = []
    for i in range(10):
        my_fishes.append(Pet("fish"))
    my_ant = Pet("ant")
    team1.add_pet(my_fishes[0], 0)
    team1.add_pet(my_fishes[1], 1)
    team1.add_pet(my_fishes[2], 2)
    team1.add_pet(my_fishes[3], 3)
    team1.add_pet(my_fishes[4], 4)
    team2.add_pet(my_ant, 0)
    team2.add_pet(my_fishes[6], 1)
    team2.add_pet(my_fishes[7], 2)
    team2.add_pet(my_fishes[8], 3)
    team2.add_pet(my_fishes[9], 4)
    base_battleground = create_battleground(team1, team2)

    # 0 = main menu
    # 1 = shop
    # 2 = battle screen
    screen = 0

    running = True
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    while running:
        pygame.event.get()
        pygame.display.flip()
        if screen == 0:
            window.blit(main_menu_bg, (0, 0))

        elif screen == 1:
            window.fill(red)
        else:
            display_battle(base_battleground)

        # event handling here
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if screen == 2:
                        print("what up")
                        battle(team1, team2)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                print(x)
                print(y)
                print("\n")
                screen += 1
                if screen == 3:
                    screen = 0
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.quit()


if __name__ == "__main__":
    main()
