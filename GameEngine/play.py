from functools import wraps
import signal
import os


TIMEOUT = 5
if 'TESTING' in os.environ:
    TIMEOUT = 1


class Update():
    def __init__(self, your_move=False, opponent_move=False, moves=0):
        self.your_move = your_move
        self.opponent_move = opponent_move
        self.moves = moves

    def deep_copy(self):
        return Update(self.your_move, self.opponent_move, self.moves)

    def update(self, your_move, opponent_move):
        self.your_move = your_move
        self.opponent_move = opponent_move
        self.moves += 1


class TimeoutError(Exception):
    pass


def timeout():
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(TIMEOUT)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


@timeout()
def play_match(bot, update):
    try:
        return bot.play(update)
    except Exception as e:
        return e


def get_scores(result_a, result_b):
    if result_a and result_b:
        return (3, 3)
    elif result_a and not result_b:
        return (1, 3)
    elif not result_a and result_b:
        return (3, 1)
    return (2, 2)


def play_game(bot_a, bot_b, iterations=1000):
    update_a = Update()
    update_b = Update()
    score = (0, 0)

    for i in range(iterations):
        result_a = play_match(bot_a, update_a.deep_copy())
        result_b = play_match(bot_b, update_b.deep_copy())

        if type(result_a) == Exception:
            return -1
        elif type(result_b) == Exception:
            return -2

        update_a.update(result_a, result_b)
        update_b.update(result_b, result_a)

        scores = get_scores(result_a, result_b)
        score = (score[0] + scores[0], score[1] + scores[1])

    return score
