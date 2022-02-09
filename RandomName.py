import random


# 18 char limit pls

# wins
def generateRandomNameSingular():
    list = ["Arcade Fire", "Team 10", "VSauce", "Pizza Time", "Boonk Gang", "Joe Rogan", "Chaos Incarnate",
            "Team Rocket", "The Mongol Horde", "A Mormon Family", "Racist Mario", "Papito", "The Locust Swarm",
            "The NAACP", "North Korean National SAP Team", "Nothing Happened at Tiananmen Square on June 6th, 1989."]
    return random.choice(list)


# win
def generateRandomNamePlural():
    list = ["Ass Eaterz", "The Liberals", "Johnny's Boys", "The Bitch Fuckers", "Clout Warriors",
            "Michael & the Motorcycles", "The Defiled", "Several Bees", "Malcolm & the Sutcliffes", "Rhino Hunters",
            "The Batmen", "The Suckboiz", "McGill Redmen", "The Toe Suckers", "The Adult Virgins", "Limp Dickbutts"]
    return random.choice(list)
