from tempfile import mkdtemp
import os

SECRET_KEY = b'CKRTQI'
TESTING = True
SERVER_NAME = 'pypriz.local:5000'

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/testa.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

BOT_FOLDER = mkdtemp()
