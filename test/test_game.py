from unittest import TestCase
import time

import GameEngine.play as game


class TrueBot():
    def play(self, update):
        return True


class FalseBot():
    def play(self, update):
        return False


class ErrorBot():
    def play(self, update):
        raise Exception


class TimeBot():
    def play(self, update):
        time.sleep(2)


class PlayTestCase(TestCase):

    def setUp(self):
        self.update = game.Update()

    def tearDown(self):
        pass

    def test_play_match(self):
        bot = TrueBot()
        result = game.play_match(bot, self.update)
        self.assertEqual(result, True)

    def test_play_match_error(self):
        bot = ErrorBot()
        result = game.play_match(bot, self.update)
        self.assertEqual(type(result), Exception)

    def test_play_match_timeout(self):
        bot = TimeBot()
        result = game.play_match(bot, self.update)
        self.assertEqual(type(result), game.TimeoutError)

    def test_get_scores(self):
        self.assertEqual(game.get_scores(False, False), (2, 2))
        self.assertEqual(game.get_scores(True, False), (1, 3))
        self.assertEqual(game.get_scores(False, True), (3, 1))
        self.assertEqual(game.get_scores(True, True), (3, 3))

    def test_play_game(self):
        bot_a = TrueBot()
        bot_b = FalseBot()

        score = game.play_game(bot_a, bot_b, 10)
        self.assertEqual(score, (10, 30))

    def test_play_game_error(self):
        error_bot = ErrorBot()
        true_bot = TrueBot()

        score = game.play_game(error_bot, true_bot, 10)
        self.assertEqual(score, -1)

        score = game.play_game(true_bot, error_bot, 10)
        self.assertEqual(score, -2)
