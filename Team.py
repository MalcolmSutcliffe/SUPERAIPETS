class Team:
    pets

    def __init__ (pets):
        self.pets = [None for i in range(5)]

    def add_pet(new_pet, pos):
        if self.pets[pos] == None:
            self.pets[pos] = new_pet
            return 1
        return 0

     def sell_pet(pos):
         if !(self.pets[pos] == None):
            self.pets[pos] = None
            return 1
        return 0

    def combine_pet(new_pet, pos):
        if self.pets[pos] == None:
            return -1
        else if !(self.pets[pos].name_tag == new_pet.name_tag):
            return 0
        else:
            new_attack = max(new_pet.get_base_attack, self.pets[pos].get_base_attack) + 1
            new_hp = max(new_pet.get_base_health, self.pets[pos].get_base_health) + 1
            self.pets[pos].set_base_attack(new_attack)
            self.pets[pos].set_base_health(new_health)
            self.pets[pos].gain_exp(1)
