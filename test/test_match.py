from multiprocessing import Queue

from unittest import TestCase

from pypriz.GameEngine.match import PlayProcess
from pypriz.GameEngine.match import Update
from pypriz.GameEngine.match import play_match 


class SlowBot():
    def play(self, update):
        for i in range(200000):
            for j in range(200000):
                i * j
        return False


class HogBot():
    def play(self, update):
        return False


class Bot():
    def __init__(self, response=False):
        self.response = response

    def play(self, update):
        return self.response


class TestMatch(TestCase):
    def test_cpu_limit(self):
        response_queue = Queue()
        response_queue.put(1)
        response_queue.get()
        play_process = PlayProcess(SlowBot(), Update(), response_queue)
        play_process.start()
        play_process.join()

        pid, error = response_queue.get()
        self.assertEqual(OSError, error)

    def test_play_match(self):
        score = play_match(Bot(), Bot(), 1)
        self.assertEqual(score, (2, 2))

        score = play_match(Bot(), Bot(True), 1)
        self.assertEqual(score, (3, 1))

        score = play_match(Bot(True), Bot(), 1)
        self.assertEqual(score, (1, 3))

        score = play_match(Bot(True), Bot(True), 1)
        self.assertEqual(score, (3, 3))
