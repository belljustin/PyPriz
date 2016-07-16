import bcrypt
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session

from pypriz.models import db
from pypriz.models.user import User

from pypriz.views import index, auth, upload

def create_app(config_filename):
    app = Flask(__name__)

    app.config.from_object(config_filename)

    app.add_url_rule('/', view_func=index.IndexView.as_view('index'))

    app.add_url_rule(
        '/login',
        view_func=auth.LoginView.as_view('login'),
        methods=['GET', 'POST'])
    app.add_url_rule(
        '/register',
        view_func=auth.RegisterView.as_view('register'),
        methods=['POST'])
    app.add_url_rule(
        '/logout',
        view_func=auth.LogoutView.as_view('logout'))

    app.add_url_rule(
        '/upload',
        view_func=upload.UploadView.as_view('upload', app.config['BOT_FOLDER']),
        methods=['POST'])

    return app
