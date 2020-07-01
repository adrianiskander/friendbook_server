from django.test import TestCase

from ..forms import PostForm


class PostFormTestCase(TestCase):

    def test_post_form_exists(self):
        self.assertIsNotNone(PostForm)
