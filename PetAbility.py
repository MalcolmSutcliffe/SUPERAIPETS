import json


class PetAbility:

    def __init__(self, pet_tag, level):

        f = open("SAPinfo.json")
        data = json.load(f)
        f.close()

        self.ability_data = None
        self.name = pet_tag

        try:
            self.ability_data = data.get("pets").get(pet_tag).get("level"+str(level)+"Ability")
        except AttributeError:
            print("Error: the pet tag '" + pet_tag + "' does not exist!")

        self.description = self.ability_data.get("description")
        self.trigger = self.ability_data.get("trigger")
        self.triggered_by = self.ability_data.get("triggeredBy").get("kind")
        self.effect_type = self.ability_data.get("effect").get("type")

    def generate_ability_function(self):

        def ability():
            print(self.name + " used ability!")

        if self.effect_type == "ModifyStats":
            target =