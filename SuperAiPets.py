import pygame
import os
from Battleground import *
from Team import Team
from Pet import Pet

# initialize the pygame module
pygame.display.init()
pygame.font.init()
# load and set the logo
pygame.display.set_caption("SUPERAIPETS")

# create window
window = pygame.display.set_mode((1280, 720))
main_menu_bg = pygame.image.load(os.path.join('images', 'main_menu.png'))


def display_battle(bg_object):
    pygame.display.flip()
    window.fill((0, 255, 0))
    for i, x in enumerate(bg_object.team1.get_pets()):
        if x is not None:
            window.blit(x.leftSprite, ((150 + (94 * i)), 300))

    for i, x in enumerate(bg_object.team2.get_pets()):
        if x is not None:
            window.blit(x.rightSprite, ((150 + (94 * (9-i))), 300))


def main():

    # f = open("SAPinfo.json")
    # data = json.load(f)
    # f.close()
    # for i in data.get("pets"):
    #     print(i)
    # print(data.get("pets").get("pet-ant").get("level1Ability"))

    team1 = Team()
    team2 = Team()
    my_fish = Pet("fish")
    my_ant = Pet("ant")
    my_cow = Pet("cow")
    my_dog = Pet("dog")
    my_beetle = Pet("beetle")
    my_lobster = Pet("lobster")
    my_kangaroo = Pet("kangaroo")
    my_camel = Pet("camel")
    my_spider = Pet("spider")
    my_sheep = Pet("sheep")
    my_dragon = Pet("dragon")
    team1.add_pet(my_fish, 0)
    team1.add_pet(my_beetle, 1)
    team1.add_pet(my_cow, 2)
    team1.add_pet(my_dragon, 3)
    team1.add_pet(my_ant, 4)
    team2.add_pet(my_lobster, 0)
    team2.add_pet(my_kangaroo, 1)
    team2.add_pet(my_sheep, 2)
    team2.add_pet(my_spider, 3)
    team2.add_pet(my_camel, 4)
    base_battleground = Battleground(team1, team2)

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
                        base_battleground.battle()
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
