import json

class PetAbility:

    def __init__(self, pet_tag, level):

        f = open("SAPinfo.json")
        data = json.load(f)
        f.close()

        try:
            ability = data.get("pets").get(pet_tag).get("level"+str(level)+"Ability")
        except AttributeError:
            print("Error: the pet tag '" + pet_tag + "' does not exist!")
