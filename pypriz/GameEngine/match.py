import resource
import os
from signal import signal, SIGXCPU
from multiprocessing import Process, Queue

MAX_RUNTIME = 5
MAX_MEMSIZE = 100*10**6


class Update:
    def __init__(self):
        self.your_move = None
        self.opponent_move = None
        self.moves = 0

    def update(self, your_move, opponent_move, move):
        self.your_move = your_move
        self.opponent_move = opponent_move
        self.move = move


def time_expired(n, stack):
    raise Exception()


class PlayProcess(Process):
    def __init__(self, bot, update, responseQueue):
        super(PlayProcess, self).__init__()
        self.bot = bot
        self.update = update
        self.responseQueue = responseQueue

    def run(self):
        try:
            signal(SIGXCPU, time_expired)
            soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
            resource.setrlimit(resource.RLIMIT_CPU, (MAX_RUNTIME, hard))

            soft, hard = resource.getrlimit(resource.RLIMIT_AS)
            resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMSIZE, hard))

            self.responseQueue.put((os.getpid(), self.bot.play(self.update)))
        except Exception as e:
            print(e, type(e))
            self.responseQueue.put((os.getpid(), e))
        finally:
            return


def get_points(responseA, responseB):
    if responseA and responseB:
        return (3, 3)
    elif responseA and not responseB:
        return (1, 3)
    elif not responseA and responseB:
        return (3, 1)
    return (2, 2)


def play_match(bot_a, bot_b, iterations):
    score = (0, 0)
    update_a, update_b = (Update(), Update())
    responseQueue = Queue()

    for i in range(iterations):
        process_a = PlayProcess(bot_a, update_a, responseQueue)
        process_b = PlayProcess(bot_b, update_b, responseQueue)

        process_a.start()
        process_b.start()
        process_a.join()
        process_b.join()

        response_a, response_b = (None, None)
        while not responseQueue.empty():
            response = responseQueue.get()
            if response[0] == process_a.pid:
                response_a = response[1]
            else:
                response_b = response[1]

        if type(response_a) != bool or type(response_b) != bool:
            raise Exception 

        points = get_points(response_a, response_b)
        score = (score[0] + points[0], score[1] + points[1])
        update_a.update(response_a, response_b, i)
        update_a.update(response_b, response_a, i)

    return score

