from pprint import pprint

from enum import Enum
from SAP_Data import *
import time


# inputs: trigger_type = a TRIGGER, trigger_from = the pet object  causing the trigger, battleground: the
# battleground that this trigger is happening on
# will send the proper triggers to all the pets on the battleground, and the pet's ability logic will decide to
# perform the ability or not.
# want to change to just send_triggers
def send_triggers(trigger_type, trigger_from, zone):
    # if trigger happens on a battlefield
    trigger_index = -1

    # Player Trigger
    if trigger_from is None:
        for x in zone.get_all_pets():
            if x is not None:
                x.receive_trigger([trigger_type, TRIGGERED_BY.Player], None)
        return

    team = trigger_from.get_battleground_team()
    if team is None:
        team = trigger_from.get_team()

    try:
        trigger_index = team.get_pets().index(trigger_from)
    except ValueError:
        pass

    # check if the index is in range
    if not 0 <= trigger_index <= 4:
        # print("Error: index" + str(trigger_index) + " out of bounds.")
        return

    # EachFriend (excluding self)
    trigger = [trigger_type, TRIGGERED_BY.EachFriend]

    for j, x in enumerate(team.get_pets()):
        if x is not None and not j == trigger_from:
            x.receive_trigger(trigger, trigger_from)

    # FriendAhead
    trigger = [trigger_type, TRIGGERED_BY.FriendAhead]
    if 1 <= trigger_index <= 4:
        for j in range(trigger_index):
            x = team.get_pets()[trigger_index - 1 - j]
            if x is not None:
                x.receive_trigger(trigger, trigger_from)
                break

    # Self
    trigger = [trigger_type, TRIGGERED_BY.Self]
    trigger_from.receive_trigger(trigger, trigger_from)


class AbilityManager:

    def __init__(self, battleground):
        self.ability_queue = []
        self.battleground = battleground

    def add_to_queue(self, ability_instance):
        self.ability_queue.append(ability_instance)

    def perform_abilities(self):
        while len(self.ability_queue) > 0:
            self.ability_queue.sort()
            self.ability_queue.pop(0).execute()
            self.battleground.display()
            time.sleep(GAME_SPEED)

    def force_ability(self, pet_ability):
        if self.ability_queue.remove(pet_ability):
            pet_ability.execute()

