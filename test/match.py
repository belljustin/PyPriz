from sys import platform

from test_bots.hogbot import Bot as BotA
from test_bots.slowbot import Bot as BotB
from match import play_match

def main():
    if platform != 'linux' and platform != 'linux2':
        print("ERROR: this test must be run on a linux box")
        return

    botA = BotA()
    botB = BotB()

    print(play_match(botA, botB, 1))

if __name__ == "__main__":
    main()
