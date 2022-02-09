from Pet import Pet

name = "Ant"
tag = "pet-ant"
pet_id = 1
base_health = 1
base_attack = 2


class ant(Pet):

    def __init__(self):
        super().__init__(base_health, base_attack, 1, None)
