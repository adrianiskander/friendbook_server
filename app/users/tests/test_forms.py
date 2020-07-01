from django.test import TestCase

from . import const
from ..forms import AuthForm


class FormsTestCase(TestCase):

    def setUp(self):
        self.form = AuthForm(const.AUTH_DATA)

    def test_form_is_valid(self):
        self.assertTrue(self.form.is_valid())
