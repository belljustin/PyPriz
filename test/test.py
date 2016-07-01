from unittest import TestCase

from pypriz.app import create_app
from pypriz.model import db

class TestApp(TestCase):

    def setUp(self):
        app = create_app('settings')
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

