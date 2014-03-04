import doctest

from django.test import TestCase

from challenge.contest import logic


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(logic))
    return tests


class ViewTestCase(TestCase):
    def test_index(self):
        request = self.client.get('/')
        self.assertEqual(request.status_code, 200)
