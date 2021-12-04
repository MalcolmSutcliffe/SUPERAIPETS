from pprint import pprint

from Battleground import *
from enum import Enum
from SAP_Data import GAME_SPEED
from SuperAiPets import *


class TRIGGER(Enum):
    AfterAttack = 1                         # implemented
    BeforeAttack = 2                        # implemented
    Buy = 3
    BuyAfterLoss = 4
    BuyFood = 5
    BuyTier1Animal = 6
    CastsAbility = 7
    EatsShopFood = 8
    EndOfTurn = 9
    EndOfTurnWith2PlusGold = 10
    EndOfTurnWith3PlusGold = 11
    EndOfTurnWith4OrLessAnimals = 12
    EndOfTurnWithLvl3Friend = 13
    Faint = 14                              # implemented
    Hurt = 15                               # implemented
    KnockOut = 16
    LevelUp = 17
    Sell = 18
    StartOfBattle = 19                      # implemented
    StartOfTurn = 20
    Summoned = 21


class TRIGGERED_BY(Enum):
    EachFriend = 1                          # implemented
    EachFriendInShop = 2
    FriendAhead = 3                         # implemented
    Player = 4                              # implemented
    Self = 5                                # implemented


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
            x.receive_trigger([trigger_type, TRIGGERED_BY.Player], None)
            return

    team = trigger_from.get_battleground_team()
    if team is None:
        team = trigger_from.get_team()

    try:
        trigger_index = team.get_pets().index(trigger_from)
    except Exception:
        pass

    # check if the index is in range
    if not 0 <= trigger_index <= 4:
        # print("Error: index" + str(trigger_index) + " out of bounds.")
        return

    # EachFriend (excluding self)
    trigger = [trigger_type, TRIGGERED_BY.EachFriend]

    for i, x in enumerate(team.get_pets()):
        if x is not None and not i == trigger_from:
            x.receive_trigger(trigger, trigger_from)

    # FriendAhead
    trigger = [trigger_type, TRIGGERED_BY.FriendAhead]
    if 1 <= trigger_index <= 4:
        for i in range(trigger_index):
            x = team.get_pets()[trigger_index - 1 - i]
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
            print("before sorting: ")
            for x in self.ability_queue:
                print("\t" + str(x))
            self.ability_queue.sort()
            print("after sorting: ")
            for x in self.ability_queue:
                print("\t" + str(x))
            self.ability_queue.pop(0).execute()
            self.ability_queue.sort()
            self.battleground.display()
            time.sleep(GAME_SPEED)
