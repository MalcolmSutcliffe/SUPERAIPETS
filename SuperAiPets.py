import random

import pygame
import os
from Fonts import *
from Battleground import *
from Team import Team
from Pet import Pet
from Status import STATUS
from SAP_Data import *
from RandomName import *


# initialize the pygame module
pygame.display.init()
pygame.font.init()
tie_render = mc75.render("It's a Draw!", False, (255, 255, 255))
tie_rect = tie_render.get_rect(center=(SCREEN_WIDTH/2, 200))
# load and set the logo
pygame.display.set_caption("SUPERAIPETS")
tflist = [0,1]

# create window
window = pygame.display.set_mode((1280, 720))
battle_bg = pygame.image.load(os.path.join('images', 'battle_bg.png'))

# direction: 0 = left, 1 = right
def display_pet(pet, direction, xpos, ypos):
    window.blit(pet.get_sprite(direction), (xpos, ypos))
    name = mc15.render(pet.name, False, (255, 255, 255))
    pet_attack_hp = mc10.render("AD: " + str(pet.get_attack()) + "   HP: " + str(pet.get_health()), False, (255, 255, 255))
    status = mc10.render(str(pet.status)[7:], False, (255, 255, 255))
    level = mc10.render("lvl: " + str(pet.get_level()), False, (255, 255, 255))
    window.blit(status, (xpos + 20, ypos))
    window.blit(name, (xpos + 20, ypos - 40))
    window.blit(level, (xpos + 20, ypos - 20))
    window.blit(pet_attack_hp, (xpos + 32, ypos + 135))


def display_team_in_battle(is_friendly, team):
    if is_friendly:
        direction = 0
        for i, x in enumerate(team.get_pets()):
            if x is not None:
                display_pet(x, direction, (25 + (120 * i)), 400)
    else:
        direction = 1
        for i, x in enumerate(team.get_pets()):
            if x is not None:
                display_pet(x, direction, (50 + (120 * (9 - i))), 400)


def display_battle(bg_object):
    pygame.display.flip()
    window.blit(battle_bg, (0, 0))
    display_team_in_battle(True, bg_object.get_team1())
    display_team_in_battle(False, bg_object.get_team2())
    winner = bg_object.get_winner()
    if winner == 1:
        window.blit(bg_object.get_team1().get_name_render(), bg_object.get_team1().get_name_render_rect())
    elif winner == 2:
        window.blit(bg_object.get_team2().get_name_render(), bg_object.get_team2().get_name_render_rect())
    elif winner == 3:
        window.blit(tie_render, tie_rect)
    else:
        return


def generate_random_team():    
    plural = random.choice(tflist)
    if plural == 0:
        return_team = Team(generateRandomNameSingular(),False)
    else:
        return_team = Team(generateRandomNamePlural(),True)
    for i in range(5):
        new_pet = Pet(random.sample(random.sample(ANIMAL_TIERS, 1)[0], 1)[0][4:])
        new_pet.set_level(random.randint(1, 3))
        return_team.add_pet(new_pet,i)
    return return_team


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

    team1 = generate_random_team()
    team2 = generate_random_team()
  

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
                    team1 = generate_random_team()
                    team2 = generate_random_team()
                    base_battleground = Battleground(team1, team2)
                    screen = 0
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.quit()


if __name__ == "__main__":
    main()
