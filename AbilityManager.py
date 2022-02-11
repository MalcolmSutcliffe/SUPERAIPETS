from pprint import pprint

from enum import Enum
from SAP_Data import *
import time


# inputs: trigger_type = a TRIGGER, trigger_from = the pet object  causing the trigger, battleground: the
# battleground that this trigger is happening on
# will send the proper triggers to all the pets on the battleground, and the pet's ability logic will decide to
# perform the ability or not.
# want to change to just send_triggers


class AbilityManager:

    def __init__(self, location):
        self.ability_queue = []
        self.location = location

    def send_triggers(self, trigger_type, trigger_from):
        # if trigger happens on a battlefield
        trigger_index = -1

        # Player Trigger
        if trigger_from is None:
            for x in self.location.get_all_pets():
                if x is not None:
                    x.receive_trigger([trigger_type, TRIGGERED_BY.Player], None)
            return

        team = trigger_from.get_team()
        if team is None:
            return

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

    def add_to_queue(self, ability_instance):
        self.ability_queue.append(ability_instance)

    def perform_abilities(self):
        while len(self.ability_queue) > 0:
            self.ability_queue.sort()
            self.ability_queue.pop(0).execute()
            self.location.display()
            time.sleep(GAME_SPEED)

    def force_ability(self, pet):
        if pet.get_ability() in self.ability_queue:
            pet.get_ability().execute()
            self.ability_queue.remove(pet.get_ability())


