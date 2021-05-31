import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    """Esta clase es la encargada de las pruebas. cada método que empieze con test_ es una prueba."""
    def setUp(self):
        self.app = create_app('testing')  # Esta es la app factory.
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
