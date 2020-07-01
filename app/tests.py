from django.test import TestCase

from app.asgi import application as asgi_app
from app.wsgi import application as wsgi_app


class TestAppSetup(TestCase):

    def setUp(self):
        self.wsgi_app = wsgi_app
        self.asgi_app = asgi_app

    def test_app_exists(self):
        self.assertIsNotNone(asgi_app, object)
        self.assertIsNotNone(wsgi_app, object)
