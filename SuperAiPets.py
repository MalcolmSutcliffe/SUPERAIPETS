import random

import pygame
import os
from Battleground import *
from Team import Team
from Pet import Pet
from Status import STATUS
from SAP_Data import *


# initialize the pygame module
pygame.display.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
myfont1 = pygame.font.SysFont('Comic Sans MS', 15)
# load and set the logo
pygame.display.set_caption("SUPERAIPETS")

# create window
window = pygame.display.set_mode((1280, 720))
battle_bg = pygame.image.load(os.path.join('images', 'battle_bg.png'))

# direction: 0 = left, 1 = right
def display_pet(pet, direction, xpos, ypos):
    window.blit(pet.get_sprite(direction), (xpos, ypos))
    name = myfont1.render(pet.name, False, (0, 0, 0))
    pet_attack = myfont.render("AD: " + str(pet.get_attack()), False, (0, 0, 0))
    pet_hp = myfont.render("HP: " + str(pet.get_health()), False, (0, 0, 0))
    status = myfont.render(str(pet.status)[7:], False, (0, 0, 0))
    level = myfont.render("lvl: " + str(pet.get_level()), False, (0, 0, 0))
    window.blit(status, (xpos + 20, ypos))
    window.blit(name, (xpos + 20, ypos - 40))
    window.blit(level, (xpos + 20, ypos - 20))
    window.blit(pet_attack, (xpos + 32, ypos + 135))
    window.blit(pet_hp, (xpos + 62, ypos + 135))


def display_team_in_battle(is_friendly, team):
    if is_friendly:
        direction = 0
        for i, x in enumerate(team.get_pets()):
            if x is not None:
                display_pet(x, direction, (125 + (94 * i)), 400)
    else:
        direction = 1
        for i, x in enumerate(team.get_pets()):
            if x is not None:
                display_pet(x, direction, (175 + (94 * (9 - i))), 400)


def display_battle(bg_object):
    pygame.display.flip()
    window.blit(battle_bg, (0, 0))
    display_team_in_battle(True, bg_object.get_team1())
    display_team_in_battle(False, bg_object.get_team2())


def generate_random_team():
    random_pet = []
    for i in range(10):
        random_pet.append(Pet(random.sample(random.sample(ANIMAL_TIERS, 1)[0], 1)[0][4:]))
        random_pet[i].set_level(random.sample([1,2,3],1)[0])
    return random_pet

def main():

    main_menu_normal = pygame.image.load(os.path.join('images', 'main_menu.png'))
    main_menu_pressed = pygame.image.load(os.path.join('images', 'main_menu_pressed.png'))
    main_menu_bg = main_menu_normal

    # for i in DATA.get("statuses"):
    #     print(i)
    # print(DATA.get("pets").get("pet-ant").get("level1Ability"))

    # print(ANIMAL_TIERS)

    
##    my_fish = Pet("fish")
##    my_ant = Pet("ant")
##    my_cow = Pet("cow")
##    my_caterpillar = Pet("caterpillar")
##    my_crab = Pet("crab")
##    my_dog = Pet("dog")
##    my_hippo = Pet("hippo")
##    my_beetle = Pet("beetle")
##    my_lobster = Pet("lobster")
##    my_kangaroo = Pet("kangaroo")
##    my_camel = Pet("camel")
##    my_spider = Pet("spider")
##    my_sheep = Pet("sheep")
##    my_dragon = Pet("dragon")
##    my_deer = Pet("deer")
##    my_turtle = Pet("turtle")
##    my_badger = Pet("badger")
##    my_blowfish = Pet("blowfish")
##    my_rhino = Pet("rhino")
##    my_fly = Pet("fly")
##    my_tiger = Pet("tiger")
##    my_snake = Pet("snake")
##    my_whale = Pet("whale")
##    my_skunk = Pet("skunk")
##    my_eagle = Pet("eagle")
##    my_leopard = Pet("leopard")
##    my_turtle.set_level(2)
##    my_octopus = Pet("octopus")
##    my_octopus.set_level(3)
##    my_eagle.set_level(2)
##    my_dragon.set_status(STATUS.GARLIC_ARMOR)
##    my_caterpillar.set_level(3)
    # my_sheep.set_status(STATUS.MELON_ARMOR)


    team1 = Team()
    team2 = Team()
    random_pet_list = generate_random_team()
    for i in range(5):
        team1.add_pet(random_pet_list[i], i)
        team2.add_pet(random_pet_list[i + 5], i)

    # print(random_pet[i])
    # print(random_pet[i+5])

    # team1.add_pet(my_hippo, 0)
    # team1.add_pet(my_caterpillar, 1)
    # team1.add_pet(my_fish, 2)
    # team1.add_pet(my_crab, 3)
    # team1.add_pet(my_dragon, 4)
    # team2.add_pet(my_kangaroo, 0)
    # team2.add_pet(my_dog, 1)
    # team2.add_pet(my_deer, 2)
    # team2.add_pet(my_whale, 3)
    # team2.add_pet(my_eagle, 4)

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
                        if team1.has_units() and team2.has_units():
                            base_battleground.battle()
                if event.key == pygame.K_d:
                    toggle_debug()
                    print
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouseX = pos[0]
                mouseY = pos[1]
                if screen == 0 and mouseX >= 266 and mouseX <= 1017 and mouseY >= 159 and mouseY <= 368:
                    main_menu_bg = main_menu_pressed
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                mouseX = pos[0]
                mouseY = pos[1]
##                print(mouseX)
##                print(mouseY)
##                print("\n")
                if screen == 0 and mouseX >= 266 and mouseX <= 1017 and mouseY >= 159 and mouseY <= 368:
                    screen = 1
                    main_menu_bg = main_menu_normal
                elif screen == 1:
                    screen = 2
                elif screen == 2:
                    random_pet_list = generate_random_team()
                    team1 = Team()
                    team2 = Team()
                    for i in range(5):
                        team1.add_pet(random_pet_list[i], i)
                        team2.add_pet(random_pet_list[i + 5], i)
                    base_battleground = Battleground(team1, team2)
                    screen = 0
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.quit()


if __name__ == "__main__":
    main()
