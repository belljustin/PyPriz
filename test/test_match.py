from sys import platform
from unittest import TestCase

from test.bots.hogbot import Bot as HogBot
from test.bots.slowbot import Bot as SlowBot
from test.bots.boilerbot import Bot as BoilerBot
from pypriz.GameEngine.match import play_match


class TestMatch(TestCase):
    @classmethod
    def setUpClass(self):
        assert platform == 'linux' or platform == 'linux2'

    def test_cpu_limit(self):
        bot = BoilerBot()
        slowbot = SlowBot()

        with self.assertRaises(Exception):
            play_match(bot, slowbot, 1)

    def test_memory_limt(self):
        bot = BoilerBot()
        hogbot = HogBot()

        with self.assertRaises(Exception):
            play_match(bot, hogbot, 1)
