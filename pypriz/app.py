import bcrypt
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session

from pypriz.model import db
from pypriz.model.user import User

from pypriz.views import index, auth, upload

def create_app(config_filename):
    app = Flask(__name__)

    app.config.from_object(config_filename)

    app.add_url_rule('/', view_func=index.IndexView.as_view('index'))

    login_view = auth.LoginView.as_view('login')
    app.add_url_rule('/login', view_func=login_view, methods=['GET', 'POST'])
    logout_view = auth.LogoutView.as_view('logout')
    app.add_url_rule('/logout', view_func=logout_view)

    upload_view = upload.UploadView.as_view('upload', app.config['BOT_FOLDER'])
    app.add_url_rule('/upload', view_func=upload_view, methods=['POST'])

    return app

if __name__ == '__main__':
    app = create_app('pypriz.settings')
    db.init_app(app)
    app.run()
