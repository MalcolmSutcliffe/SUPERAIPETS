class Pet
    name_tag
    image
    base_attack
    base_health
    temp_attack
    temp_health
    attack
    health
    experience
    item

    #fucntion perform_ability @override

    def __init__(base_attack, base_health, temp_attack=0,temp_health=0,exp=0, item=NULL):
        self.base_attack = base_attack
        self.base_health = base_health
        self.temp_attack = temp_attack
        self.temp_health = temp_health
        self.attack = base_attack + temp_attack
        self.health = base_health + temp_health
        if attack > 50:
            attack = 50
        if health > 50:
            health = 50
        self.item = item

    def perform_ability():
        #ability goes here

    def get_dmg():

        dmg = attack

        if item is MEAT_BONE:
            dmg += 5

        if item is STEAK:
            dmg += 20
            item.set_active(0)

        return dmg

    def take_damage(dmg):

        if item is GARLIC_ARMOR:
            if dmg <= 3:
                dmg = 1
            else
                dmg -= 2

        if item is MELON_ARMOR:
            dmg -= 20
            item.set_active(0)

        if dmg < 0:
            dmg = 0

        health -= dmg

        if health <= 0:
            die()

    def die():
        #idk, probably better to do in battle

    def gain_stats(stats, stat_type=0): #(0 = permanent stats, #1 = temp stat)
        if stat_type==0:
            self.base_attack += stats[0]
            self.base_health += stats[1]
        if stat_type==1:
            self.temp_attack += stats[0]
            self.temp_health += stats[1]

    def gain_exp(exp):
        self.experience += exp

    #getters and setters
    def get_attack():
        return self.attack

    def get_health():
        return self.health

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
