import copy
import random
import ptext
import pygame
import os
from Battleground import *
from Team import Team
from Pet import Pet, generate_random_pet
from Shop import Shop
from Status import STATUS
from SAP_Data import *
import webbrowser

# initialize the pygame module
pygame.display.init()
pygame.font.init()
# load and set the logo
pygame.display.set_caption("SUPERAIPETS")
ptext.FONT_NAME_TEMPLATE = "fonts/%s.otf"

bottom_offset = SCREEN_HEIGHT - 20
right_offset = SCREEN_WIDTH - 20

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# create window
window = pygame.display.set_mode((1280, 720))
battle_bg = pygame.image.load(os.path.join('images', 'battle_bg.png'))


# direction: 0 = left, 1 = right
def display_pet(pet, direction, xpos, ypos):
    window.blit(pet.get_sprite(direction), (xpos, ypos))
    ptext.draw(str(pet.status)[7:], centerx=(xpos + 64), top=ypos, fontname="Minecraftia", fontsize=15, owidth=1.5,
               ocolor=(0, 0, 0), color=(255, 255, 255))
    ptext.draw(pet.name, centerx=(xpos + 64), top=(ypos - 40), fontname="Minecraftia", fontsize=18, owidth=1.5,
               ocolor=(0, 0, 0), color=(255, 255, 255))
    ptext.draw("lvl: " + str(pet.get_level()), centerx=(xpos + 64), top=(ypos - 20), fontname="Minecraftia",
               fontsize=15, owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
    ptext.draw("AD: " + str(pet.get_attack()) + "   HP: " + str(pet.get_health()), centerx=(xpos + 64),
               top=(ypos + 128), fontname="Minecraftia", fontsize=15, owidth=1.5, ocolor=(0, 0, 0),
               color=(255, 255, 255))


def display_shop(shop):
    for i, x in enumerate(shop.team.get_pets()):
        if x is not None:
            display_pet(x, 0, (285 + (120 * i)), 200)

    for i, x in enumerate(shop.shop_animals):
        if x is not None:
            display_pet(x, 0, (285 + (120 * i)), 400)


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
    ptext.draw(bg_object.get_team1().get_name(), left=20, bottom=bottom_offset, fontname="Lapsus", fontsize=40,
               owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
    ptext.draw(bg_object.get_team2().get_name(), right=right_offset, bottom=bottom_offset, fontname="Lapsus",
               fontsize=40, owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
    if winner == 1:
        if bg_object.get_team1().is_plural():
            ptext.draw(bg_object.get_team1().get_name() + " Win!", centerx=640, top=150, fontname="Lapsus", fontsize=80,
                       owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
        else:
            ptext.draw(bg_object.get_team1().get_name() + " Wins!", centerx=640, top=150, fontname="Lapsus",
                       fontsize=80, owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
    elif winner == 2:
        if bg_object.get_team2().is_plural():
            ptext.draw(bg_object.get_team2().get_name() + " Win!", centerx=640, top=150, fontname="Lapsus", fontsize=80,
                       owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
        else:
            ptext.draw(bg_object.get_team2().get_name() + " Wins!", centerx=640, top=150, fontname="Lapsus",
                       fontsize=80, owidth=1.5, ocolor=(0, 0, 0), color=(255, 255, 255))
    elif winner == 3:
        ptext.draw("It's a draw!", centerx=640, top=150, fontname="Lapsus", fontsize=80, owidth=1.5, ocolor=(0, 0, 0),
                   color=(255, 255, 255))
    else:
        return

def main():
    # init main menu images
    main_menu_normal = pygame.image.load(os.path.join('images', 'main_menu', 'main_menu.png'))
    main_menu_play_pressed = pygame.image.load(os.path.join('images', 'main_menu', 'main_menu_play_pressed.png'))
    main_menu_settings_pressed = pygame.image.load(
        os.path.join('images', 'main_menu', 'main_menu_settings_pressed.png'))
    main_menu_reddit_pressed = pygame.image.load(os.path.join('images', 'main_menu', 'main_menu_reddit_pressed.png'))
    main_menu_twitter_pressed = pygame.image.load(os.path.join('images', 'main_menu', 'main_menu_twitter_pressed.png'))
    main_menu_bg = main_menu_normal

    settings_menu_bg = pygame.image.load(os.path.join('images', 'settings_menu', 'settings_menu.png'))
    settings_back_off = pygame.image.load(os.path.join('images', 'settings_menu', 'settings_back_off.png'))
    settings_back_on = pygame.image.load(os.path.join('images', 'settings_menu', 'settings_back_on.png'))
    game_speed_1 = pygame.image.load(os.path.join('images', 'settings_menu', 'game_speed_1.png'))
    game_speed_2 = pygame.image.load(os.path.join('images', 'settings_menu', 'game_speed_2.png'))
    game_speed_3 = pygame.image.load(os.path.join('images', 'settings_menu', 'game_speed_3.png'))
    game_speed_4 = pygame.image.load(os.path.join('images', 'settings_menu', 'game_speed_4.png'))
    game_speed_inf = pygame.image.load(os.path.join('images', 'settings_menu', 'game_speed_inf.png'))
    debug_mode_off = pygame.image.load(os.path.join('images', 'settings_menu', 'debug_mode_off.png'))
    debug_mode_on = pygame.image.load(os.path.join('images', 'settings_menu', 'debug_mode_on.png'))
    back_button_graphic = settings_back_off
    game_speed_graphic = game_speed_3
    debug_mode_graphic = debug_mode_off

    shop_menu_3_slots = pygame.image.load(os.path.join('images', 'shop_menu', 'shop_menu_3_slots.png'))
    shop_menu_4_slots = pygame.image.load(os.path.join('images', 'shop_menu', 'shop_menu_4_slots.png'))
    shop_menu_5_slots = pygame.image.load(os.path.join('images', 'shop_menu', 'shop_menu_5_slots.png'))
    exit_pressed = pygame.image.load(os.path.join('images', 'shop_menu', 'exit_pressed.png'))
    exit_unpressed = pygame.image.load(os.path.join('images', 'shop_menu', 'exit_unpressed.png'))
    fight_pressed = pygame.image.load(os.path.join('images', 'shop_menu', 'fight_pressed.png'))
    fight_unpressed = pygame.image.load(os.path.join('images', 'shop_menu', 'fight_unpressed.png'))
    exit_button = exit_unpressed
    fight_button = fight_unpressed
    shop_menu_bg = shop_menu_3_slots

    # for i in DATA.get("statuses"):
    #     print(i)
    # print(DATA.get("pets").get("pet-ant").get("level1Ability"))

    # print(ANIMAL_TIERS)

    # my_fish = Pet("fish")
    # my_ant = Pet("ant")
    # my_cow = Pet("cow")
    # my_caterpillar = Pet("caterpillar")
    # my_crab = Pet("crab")
    # my_dog = Pet("dog")
    # my_hippo = Pet("hippo")
    # my_beetle = Pet("beetle")
    # my_lobster = Pet("lobster")
    # my_kangaroo = Pet("kangaroo")
    # my_camel = Pet("camel")
    # my_spider = Pet("spider")
    # my_sheep = Pet("sheep")
    # my_dragon = Pet("dragon")
    # my_deer = Pet("deer")
    # my_turtle = Pet("turtle")
    # my_badger = Pet("badger")
    # my_blowfish = Pet("blowfish")
    # my_rhino = Pet("rhino")
    # my_fly = Pet("fly")
    # my_tiger = Pet("tiger")
    # my_snake = Pet("snake")
    # my_whale = Pet("whale")
    # my_skunk = Pet("skunk")
    # my_eagle = Pet("eagle")
    # my_leopard = Pet("leopard")
    # my_turtle.set_level(2)
    # my_octopus = Pet("octopus")
    # my_octopus.set_level(3)
    # my_eagle.set_level(2)
    # my_dragon.set_status(STATUS.GARLIC_ARMOR)
    # my_caterpillar.set_level(3)
    # my_sheep.set_status(STATUS.MELON_ARMOR)

    team1 = Team("Team Name", False)
    team1.randomize_team()
    team2 = Team("Team Name", False)
    team2.randomize_team()
    team1_healthy = copy.copy(team1)

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

    # base_shop = Shop()
    base_shop = Shop(team1)
    base_battleground = Battleground(team1, team2)

    # 0 = main menu
    # 1 = shop
    # 2 = battle screen
    # 3 = settings
    # 4 = pet selection screen
    screen = 0

    running = True

    while running:
        pygame.event.get()
        pygame.display.flip()
        # main menu
        if screen == 0:
            window.blit(main_menu_bg, (0, 0))
        # shop
        elif screen == 1:
            window.blit(shop_menu_bg, (0, 0))
            window.blit(exit_button, (0, 0))
            window.blit(fight_button, (0, 0))
            ptext.draw(str(base_shop.get_turn()), centerx=456, centery=40, fontname="Lapsus", fontsize=40, owidth=1.5,
                       ocolor=(0, 0, 0), color=(255, 255, 255))
            display_shop(base_shop)
        # battle
        elif screen == 2:
            display_battle(base_battleground)
        # settings
        elif screen == 3:
            window.blit(settings_menu_bg, (0, 0))
            window.blit(back_button_graphic, (0, 0))
            window.blit(game_speed_graphic, (0, 0))
            window.blit(debug_mode_graphic, (0, 0))
        else:
            window.fill(BLACK)

        # event handling here
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if screen == 2:
                        if base_battleground.get_team1().has_units() and base_battleground.get_team2().has_units():
                            base_battleground.battle()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouseX = pos[0]
                mouseY = pos[1]
                if screen == 0:
                    # play
                    if 266 <= mouseX <= 1017 and 159 <= mouseY <= 368:
                        main_menu_bg = main_menu_play_pressed
                    # settings
                    elif 1040 <= mouseX <= 1109 and 168 <= mouseY <= 234:
                        main_menu_bg = main_menu_settings_pressed
                    # reddit
                    elif 1201 <= mouseX <= 1268 and 551 <= mouseY <= 615:
                        main_menu_bg = main_menu_reddit_pressed
                    # twitter
                    elif 1201 <= mouseX <= 1268 and 641 <= mouseY <= 705:
                        main_menu_bg = main_menu_twitter_pressed
                elif screen == 1:
                    if 1060 <= mouseX <= 1263 and 16 <= mouseY <= 89:
                        exit_button = exit_pressed
                    elif 921 <= mouseX <= 1255 and 622 <= mouseY <= 694:
                        fight_button = fight_pressed
                elif screen == 3:
                    # back
                    if 42 <= mouseX <= 108 and 37 <= mouseY <= 102:
                        back_button_graphic = settings_back_on
                    # game speed
                    elif 490 <= mouseX <= 559 and 193 <= mouseY <= 260:
                        game_speed_graphic = game_speed_1
                        change_game_speed(1)
                    elif 647 <= mouseX <= 715 and 193 <= mouseY <= 260:
                        game_speed_graphic = game_speed_2
                        change_game_speed(2)
                    elif 803 <= mouseX <= 872 and 193 <= mouseY <= 260:
                        game_speed_graphic = game_speed_3
                        change_game_speed(3)
                    elif 959 <= mouseX <= 1029 and 193 <= mouseY <= 260:
                        game_speed_graphic = game_speed_4
                        change_game_speed(4)
                    elif 1115 <= mouseX <= 1185 and 193 <= mouseY <= 260:
                        game_speed_graphic = game_speed_inf
                        change_game_speed(0)
                    # debug mode
                    elif 494 <= mouseX <= 711 and 334 <= mouseY <= 426:
                        debug_mode_graphic = debug_mode_on
                        set_debug_mode(True)
                    elif 755 <= mouseX <= 973 and 334 <= mouseY <= 426:
                        debug_mode_graphic = debug_mode_off
                        set_debug_mode(False)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                mouseX = pos[0]
                mouseY = pos[1]
                # print("("+str(mouseX) + " , " + str(mouseY) + ") \n")
                # main menu
                if screen == 0:
                    # play
                    if 266 <= mouseX <= 1017 and 159 <= mouseY <= 368:
                        base_shop.reset()
                        base_shop.roll_shop()
                        shop_menu_bg = shop_menu_3_slots
                        screen = 1
                    # settings
                    elif 1040 <= mouseX <= 1109 and 168 <= mouseY <= 234:
                        screen = 3
                    # reddit
                    elif 1201 <= mouseX <= 1268 and 551 <= mouseY <= 615:
                        webbrowser.open('https://reddit.com/r/funko')
                    # twitter
                    elif 1201 <= mouseX <= 1268 and 641 <= mouseY <= 705:
                        webbrowser.open('https://twitter.com/JohnHinckley20')
                    main_menu_bg = main_menu_normal
                # shop
                elif screen == 1:
                    # exit
                    if 1060 <= mouseX <= 1263 and 16 <= mouseY <= 89:
                        screen = 0
                    # fight
                    elif 921 <= mouseX <= 1255 and 622 <= mouseY <= 694:
                        screen = 2
                        team2.randomize_team()
                    fight_button = fight_unpressed
                    exit_button = exit_unpressed
                # battle
                elif screen == 2:
                    base_shop.next_turn()
                    base_shop.roll_shop()
                    if base_shop.get_turn() == 5:
                        shop_menu_bg = shop_menu_4_slots
                    elif base_shop.get_turn() == 9:
                        shop_menu_bg = shop_menu_5_slots
                    screen = 1
                    base_battleground.reset_winner()
                    # team1 = copy.copy(team1_healthy)
                # settings
                elif screen == 3:
                    if 42 <= mouseX <= 108 and 37 <= mouseY <= 102:
                        screen = 0
                    back_button_graphic = settings_back_off

            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False to exit the main loop
                running = False
                pygame.quit()


if __name__ == "__main__":
    main()
