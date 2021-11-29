class Pet
    name_tag
    image
    base_attack
    base_health
    temp_attack
    temp_health
    experience
    item

    #fucntion perform_ability @override

    def __init__(base_attack, base_health, temp_attack=0,temp_health=0,exp=0, item=NULL):
        self.base_attack = base_attack
        self.base_health = base_health
        self.temp_attack = temp_attack
        self.temp_health = temp_health
        self.item = item

    def perform_ability():
        #ability goes here

    def gain_perma_stats(plus_stats):
        self.base_attack += plus_stats[0]
        self.base_health += plus_stats[1]

    def gain_temp_stats(plus_stats):
        self.temp_attack += plus_stats[0]
        self.temp_health += plus_stats[1]

    def gain_exp(exp):
        self.experience += exp

    #getters and setters
    def get_base_attack():
        return self.base_attack

    def get_base_health():
        return self.base_health

    def get_temp_attack():
        return self.temp_attack

    def get_temp_health():
        return self.temp_attack

    def get_total_attack():
        return self.base_attack + self.temp_attack

    def get_base_health():
        return self.base_health + self.temp_health

    def set_base_attack(ba):
        self.base_attack = ba

    def set_base_health(bh):
        self.base_health = bh

    def set_temp_attack(ta):
        self.temp_attack = ta

    def set_temp_health(th):
        self.temp_health = th
