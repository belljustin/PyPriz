import os
from flask import url_for
from unittest import TestCase
from functools import wraps
from tempfile import TemporaryFile

from pypriz.app import create_app
from pypriz.models import db
from pypriz.models.user import User

EMAIL = 'foo@gmail.com'
PASSWORD = 'password'
USERNAME = 'foobar'

def context_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with args[0].app.app_context():
            return f(*args, **kwargs)
    return wrapper

class TestApp(TestCase):

    def setUp(self):
        self.app = create_app('test.settings')

        self.client = self.app.test_client()

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            db.drop_all()


    def register(self, email, password, username):
        data = dict(
            email=email,
            password=password,
            username=username)
        return self.client.post(url_for('register'), data=data, follow_redirects=True)

    def login(self, email, password):
        data = dict(
            email=email,
            password=password)
        return self.client.post(url_for('login'), data=data, follow_redirects=True)

    @context_wrapper
    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

    @context_wrapper
    def test_register(self):
        response = self.register(EMAIL, PASSWORD, USERNAME)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(User.query.all())
        with self.client.session_transaction() as sess:
            self.assertTrue('user' in sess)

    @context_wrapper
    def test_logout(self):
        self.register(EMAIL, PASSWORD, USERNAME)
        response = self.client.get(url_for('logout'))
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertFalse('user' in sess)

    @context_wrapper
    def test_login(self):
        self.register(EMAIL, PASSWORD, USERNAME)
        self.client.get(url_for('logout'))
        response = self.login(EMAIL, PASSWORD)
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertTrue('user' in sess)

    @context_wrapper
    def test_upload(self):
        response = self.client.post(url_for('upload'))
        self.assertEqual(response.status_code, 302)

        self.register(EMAIL, PASSWORD, USERNAME)
        self.login(EMAIL, PASSWORD)
        tf = TemporaryFile()
        data = {'botfile': (tf, "test.txt"),
                'context_type': 'multipart/form-data'}
        response = self.client.post(url_for('upload'), data=data)
        self.assertEqual(response.status_code, 200)
        botfile = os.path.join(self.app.config['BOT_FOLDER'], '1.py')
        self.assertTrue(os.path.isfile(botfile))

