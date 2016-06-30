import bcrypt
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session

from model import db
from model.user import User

from controller import index, login, logout, upload

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('FLASK_SETTINGS')
db.init_app(app)

app.add_url_rule('/', 'index', index)
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/upload', 'upload', upload, methods=['POST'])

if __name__ == '__main__':
    app.debug = True
    app.run()
