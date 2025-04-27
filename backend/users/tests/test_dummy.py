from django.test import TestCase

class SimpleTest(TestCase):

    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_true_is_true(self):
        self.assertTrue(True)
