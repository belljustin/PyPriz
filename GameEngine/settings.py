import os


BOT_PATH = 'pypriz/bots'
if 'PYPRIZ_BOT_PATH' in os.environ:
    BOT_PATH = os.environ['PYPRIZ_BOT_PATH']
BOT_MODULE = 'pypriz.bots'
if 'PYPRIZ_BOT_PATH' in os.environ:
    BOT_MODULE = os.environ['PYPRIZ_BOT_MODULE']
