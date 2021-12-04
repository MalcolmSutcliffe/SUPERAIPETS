import random

import pygame
import os
from Battleground import *
from Team import Team
from Pet import Pet
from Status import STATUS
from SAP_Data import ANIMAL_TIERS

# initialize the pygame module
pygame.display.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
# load and set the logo
pygame.display.set_caption("SUPERAIPETS")

# create window
window = pygame.display.set_mode((1280, 720))
main_menu_bg = pygame.image.load(os.path.join('images', 'main_menu.png'))


# direction: 0 = left, 1 = right
def display_pet(pet, direction, xpos, ypos):
    window.blit(pet.get_sprite(direction), (xpos, ypos))
    pet_attack = myfont.render("AD: " + str(pet.get_attack()), False, (0, 0, 0))
    pet_hp = myfont.render("HP: " + str(pet.get_health()), False, (0, 0, 0))
    status = myfont.render(str(pet.status), False, (0, 0, 0))
    window.blit(status, (xpos+32, ypos))
    window.blit(pet_attack, (xpos+32, ypos+120))
    window.blit(pet_hp, (xpos+62, ypos+120))


def display_team_in_battle(is_friendly, team):
    if is_friendly:
        direction = 0
        for i, x in enumerate(team.get_pets()):
            if x is not None:
                display_pet(x, direction, (150 + (94 * i)), 300)
    else:
        direction = 1
        for i, x in enumerate(team.get_pets()):
            if x is not None:
                display_pet(x, direction, (150 + (94 * (9-i))), 300)


def display_battle(bg_object):
    pygame.display.flip()
    window.fill((0, 255, 0))
    display_team_in_battle(True, bg_object.get_team1())
    display_team_in_battle(False, bg_object.get_team2())


def main():

    # for i in DATA.get("statuses"):
    #     print(i)
    # print(DATA.get("pets").get("pet-ant").get("level1Ability"))

    # print(ANIMAL_TIERS)

    team1 = Team()
    team2 = Team()
    my_fish = Pet("fish")
    my_ant = Pet("ant")
    my_cow = Pet("cow")
    my_dog = Pet("dog")
    my_hippo = Pet("hippo")
    my_beetle = Pet("beetle")
    my_lobster = Pet("lobster")
    my_kangaroo = Pet("kangaroo")
    my_camel = Pet("camel")
    my_spider = Pet("spider")
    my_sheep = Pet("sheep")
    my_dragon = Pet("dragon")
    my_deer = Pet("deer")
    my_turtle = Pet("turtle")
    my_badger = Pet("badger")
    my_blowfish = Pet("blowfish")
    my_rhino = Pet("rhino")
    my_turtle.set_level(2)
    my_octopus = Pet("octopus")
    my_octopus.set_level(3)
    my_dragon.set_status(STATUS.GARLIC_ARMOR)
    # my_sheep.set_status(STATUS.MELON_ARMOR)

    random.seed(56749586465)

    random_pet = []
    for i in range(10):
        random_pet.append(Pet(random.sample(random.sample(ANIMAL_TIERS, 1)[0], 1)[0][4:]))

    for i in range(5):
        team1.add_pet(random_pet[i], i)
        team2.add_pet(random_pet[i+5], i)

    # team1.add_pet(my_fish, 0)
    # team1.add_pet(my_beetle, 1)
    # team1.add_pet(my_turtle, 2)
    # team1.add_pet(my_sheep, 3)
    # team1.add_pet(my_ant, 4)
    # team2.add_pet(my_kangaroo, 0)
    # team2.add_pet(my_dog, 1)
    # team2.add_pet(my_camel, 2)
    # team2.add_pet(my_deer, 3)
    # team2.add_pet(my_octopus, 4)

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
                        # print("what up")
                        base_battleground.battle()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                # print(x)
                # print(y)
                # print("\n")
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
