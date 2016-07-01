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
        return True

    # use data from the previous round to update your strategy
    def get_update(self, update):
        pass

    def __repr__(self):
        return name

