'''
    BoilerPlate Bot
    a.k.a. Blabby Bot
'''

class Bot:
    name = "Blabby Bot"

    # store your bot's state here
    def __init__(self):
        pass

    # define your bot's playing strategy here 
    # True = betray, False = keep quiet
    def play(self):
        for i in range(200000):
            for j in range(200000):
                v = i * j
        return False

    # use data from the previous round to update your strategy
    def get_update(self, update):
        return None

    def __repr__(self):
        return name

