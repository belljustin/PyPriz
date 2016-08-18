from multiprocessing.managers import BaseManager
from unittest import TestCase
from time import sleep

import GameEngine.server as server


class QueueManager(BaseManager):
    pass


def connectServer():
    QueueManager.register('get_queue')
    m = QueueManager(address=('127.0.0.1', 50000), authkey=b'123')
    m.connect()
    return m


def passMsg(msg):
    m = connectServer()
    queue = m.get_queue()
    queue.put(msg)


def getMsg():
    m = connectServer()
    queue = m.get_queue()
    msg = queue.get()
    return msg


class ServerTestCase(TestCase):

    def setUp(self):
        self.gs = server.GameServer()
        self.gs.start()
        sleep(0.1)

    def tearDown(self):
        self.gs.terminate()

    def test_server(self):
        passMsg('1')
