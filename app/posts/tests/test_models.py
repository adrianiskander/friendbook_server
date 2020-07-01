from django.test import TestCase

from ..models import Post


class PostModelTestCase(TestCase):

    def test_post_model_exists(self):
        self.assertIsNotNone(Post)
