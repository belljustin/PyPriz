from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from importlib import import_module
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
        super(GameManager, self).__init__()

    def run(self):
        while True:
            scores = []

            bot = self.q.get()
            other_bots = filter(lambda x: x != bot, get_bots())

            BotA = import_module(".".join([BOT_MODULE, bot]))
            for opponent in other_bots:
                BotB = import_module(".".join([BOT_MODULE, opponent]))

                bot_a = BotA.Bot()
                bot_b = BotB.Bot()
                scores.append(play_game(bot_a, bot_b))
            print(scores)


class QueueManager(BaseManager):
    pass


class GameServer(Process):
    def __init__(self):
        super(GameServer, self).__init__()

    def start_server(self):
        queue = Queue()
        g = GameManager(queue)
        g.start()

        QueueManager.register('get_queue', callable=lambda: queue)
        m = QueueManager(address=('', 50000), authkey=b'123')
        s = m.get_server()
        s.serve_forever()

    def run(self):
        self.start_server()


if __name__ == '__main__':
    with open('GameEngine/ascii_art.txt', 'r') as f:
        print(f.read())
        print("--- GameEngine ---")
    try:
        GameServer().start_server()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting Down...")
