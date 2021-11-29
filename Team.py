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
            self.pets[pos].gain_perma_stats((1,1))
            self.pets[pos].gain_exp(1)
