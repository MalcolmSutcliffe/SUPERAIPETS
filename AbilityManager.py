from Battleground import Battleground
from enum import Enum


class TRIGGER(Enum):
    AfterAttack = "AfterAttack"
    BeforeAttack = "BeforeAttack"
    Buy = "Buy"
    BuyAfterLoss = "BuyAfterLoss"
    BuyFood = "BuyFood"
    BuyTier1Animal = "BuyTier1Animal"
    CastsAbility = "CastsAbility"
    EatsShopFood = "EatsShopFood"
    EndOfTurn = "EndOfTurn"
    EndOfTurnWith2PlusGold = "EndOfTurnWith2PlusGold"
    EndOfTurnWith3PlusGold = "EndOfTurnWith3PlusGold"
    EndOfTurnWith4OrLessAnimals = "EndOfTurnWith4OrLessAnimals"
    EndOfTurnWithLvl3Friend = "EndOfTurnWithLvl3Friend"
    Faint = "Faint"
    Hurt = "Hurt"
    KnockOut = "Knockout"
    LevelUp = "LevelUp"
    Sell = "Sell"
    StartOfBattle = "StartOfBattle"
    StartOfTurn = "StartOfTurn"
    Summoned = "Summoned"


class TRIGGERED_BY(Enum):
    EachFriend = "EachFriend"
    FriendAhead = "FriendAhead"
    Player = "Player"
    Self = "Self"


# inputs: trigger_type = a TRIGGER, trigger_from = the pet object  causing the trigger, battleground: the
# battleground that this trigger is happening on
# will send the proper triggers to all the pets on the battleground, and the pet's ability logic will decide to
# perform the ability or not.
def send_triggers(trigger_type, trigger_from, space):
    # if trigger happens on a battlefield
    trigger_index = -1
    for i in range(9):
        if space[i] == trigger_from:
            trigger_index = i

    if space is Battleground:

        # check if the index is in range
        if 0 <= trigger_index <= 4:
            is_team1 = True
        elif 5 <= trigger_index <= 9:
            is_team1 = False
        else:
            print("Error: index out of bounds.")
            return

        # EachFriend (excluding self)
        trigger = [trigger_type, TRIGGERED_BY.EachFriend]

        if is_team1:
            for i in range(4):
                if space[i] is not None and not i == trigger_index:
                    space[i].recieve_trigger(trigger)
        else:
            for i in range(5, 9):
                if space[i] is not None and not i == trigger_index:
                    space[i].recieve_trigger(trigger)

        # FriendAhead
        trigger = [trigger_type, TRIGGERED_BY.FriendAhead]
        if 1 <= trigger_index <= 4:
            for i in range(trigger_index):
                if space[trigger_index - 1 - i] is not None:
                    space[i].recieve_trigger(trigger)
                    break
        if 5 <= trigger_index <= 8:
            for i in range(trigger_index - 4):
                if space[trigger_index + 1 + i] is not None:
                    space[i].recieve_trigger(trigger)
                    break

        # Self
        trigger = [trigger_type, TRIGGERED_BY.Self]
        space[trigger_index].recieve_trigger(trigger)

        # There is no player trigger in battleground (auto-battler and such)

        # if space is Shop:
        #
        #     # check if the index is in range
        #     if not 0 <= trigger_index <= 4:
        #         print("Error: index out of bounds.")
        #         return
        #
        #     # EachFriend (excluding self)
        #     trigger = [trigger_type, "EachFriend"]
        #     for i in range(4):
        #         if space[i] is not None and not i == trigger_index:
        #             space[i].recieve_trigger(trigger)
        #
        #     # FriendAhead
        #     trigger = [trigger_type, "FriendAhead"]
        #     for i in range(trigger_index):
        #         if space[trigger_index - 1 - i] is not None:
        #             space[i].recieve_trigger(trigger)
        #             break
        #
        #     # Player
        #     trigger = [trigger_type, "Player"]
        #     for i in range(4):
        #         space[i].recieve_trigger(trigger)
        #
        #     # Self
        #     trigger = [trigger_type, "Self"]
        #     space[trigger_index].recieve_trigger(trigger)


class AbilityManager:

    def __init__(self):
        self.ability_queue = []

    def add_to_queue(self, ability_instance):
        self.ability_queue.append(ability_instance)

    def perform_abilities(self):
        self.ability_queue.sort()
        for a in self.ability_queue:
            a.execute()
