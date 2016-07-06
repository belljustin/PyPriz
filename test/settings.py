import os

SECRET_KEY = b'\x01x&\x17\xd3\xb3\xedD\xe3e(\t\x97m4P\x87\x049\xd3*\xec\xdb\x88'
TESTING = True

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/testa.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

BOT_FOLDER = os.getcwd()
