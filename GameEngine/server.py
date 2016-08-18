from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from os import listdir
from re import search

from GameEngine.play import play_game
from GameEngine.settings import BOT_PATH, BOT_MODULE


def get_bots():
    files = listdir(BOT_PATH)
    return [x[:-3] for x in files if search('^[0-9]+.py$', x)]


class GameManager(Process):
    def __init__(self, q):
        self.q = q
        self.bots = get_bots()
        super(GameManager, self).__init__()

    def run(self):
        while True:
            bot = self.q.get()
            other_bots = self.bots
            self.bots = self.bots + [bot]

            bot_a = __import__(BOT_MODULE + bot)
            for opponent in other_bots:
                bot_b = __import__(".".join([BOT_MODULE, opponent]))
                print(play_game(bot_a, bot_b))


class QueueManager(BaseManager):
    pass


def start_server():
    queue = Queue()
    g = GameManager(queue)
    g.start()

    QueueManager.register('get_queue', callable=lambda: queue)
    m = QueueManager(address=('127.0.0.1', 50000), authkey=b'123')
    s = m.get_server()
    s.serve_forever()


if __name__ == '__main__':
    with open('GameEngine/ascii_art.txt', 'r') as f:
        print(f.read())
        print("--- GameEngine ---")
    start_server()
