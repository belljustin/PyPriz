from flask import url_for
from unittest import TestCase
from functools import wraps

from pypriz.app import create_app
from pypriz.model import db
from pypriz.model.user import User

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
        response = self.register('foo@gmail.com', 'password', 'bar')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(User.query.all())
        with self.client.session_transaction() as sess:
            self.assertTrue('user' in sess)

    @context_wrapper
    def test_logout(self):
        self.register('foo@gmail.com', 'password', 'bar')
        response = self.client.get(url_for('logout'))
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertFalse('user' in sess)

    @context_wrapper
    def test_login(self):
        email, password = 'foo@gmail.com', 'password'
        self.register(email, password, 'foobar')
        self.client.get(url_for('logout'))
        response = self.login(email, password)
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertTrue('user' in sess)

    #TODO: test upload

