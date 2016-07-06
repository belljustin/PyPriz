from unittest import TestCase

from pypriz.app import create_app
from pypriz.model import db

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

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

