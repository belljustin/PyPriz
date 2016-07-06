from unittest import TestCase

from pypriz.app import create_app
from pypriz.model import db
from pypriz.model.user import User

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
        return self.client.post('/register', data=data, follow_redirects=True)

    def login(self, email, password):
        data = dict(
            email=email,
            password=password)
        return self.client.post('/login', data=data, follow_redirects=True)

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.register('foo@gmail.com', 'password', 'bar')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIsNotNone(User.query.all())

    def test_login(self):
        email, password = 'foo@gmail.com', 'password'
        self.register(email, password, 'foobar')
        response = self.login(email, password)
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertTrue('user' in sess)

