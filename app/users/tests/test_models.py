from django.test import TestCase

from ..models import Account


class AccountModelTestCase(TestCase):

    def setUp(self):
        self.account = Account()

    def tearDown(self):
        pass

    def test_model_exists(self):
        self.assertIsInstance(self.account, object)
