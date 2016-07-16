from sys import platform
from unittest import TestCase

from test.bots.hogbot import Bot as HogBot
from test.bots.slowbot import Bot as SlowBot
from test.bots.boilerbot import Bot as BoilerBot
from pypriz.GameEngine.match import play_match

def main():
    if platform != 'linux' and platform != 'linux2':
        return

    botA = BotA()
    botB = BotB()

    print(play_match(botA, botB, 1))

if __name__ == "__main__":
    main()

class TestMatch(TestCase):
    @classmethod
    def setUpClass(self):
        assert platform == 'linux' or platform == 'linux2'

    def test_cpu_limit(self):
        bot = BoilerBot()
        slowbot = SlowBot()

        with self.assertRaises(Exception):
            play_match(botA, botB, 1)
