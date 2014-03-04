import doctest

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

from challenge.contest import logic

from .models import Entry


class EntryTestCase(TestCase):
    setUp = lambda self: new_user(self)

    def test_code_constraint_over(self):
        """code less than allowed chars, more than allowed bytes"""
        # 'š' is a 2-byte utf8 character
        code1 = "".join(['š'] * (settings.MAX_CODE_SIZE // 2 + 1))
        e1 = Entry.objects.create(user=self.user, code=code1)
        self.assertRaises(ValidationError, e1.full_clean)

    def test_code_constraint_just_enough(self):
        # 'š' is a 2-byte utf8 character
        code2 = "".join(['š'] * (settings.MAX_CODE_SIZE // 2))
        e2 = Entry.objects.create(user=self.user, code=code2)
        self.assertIsNone(e2.full_clean())


class ViewTestCase(TestCase):
    def test_index(self):
        request = self.client.get('/')
        self.assertEqual(request.status_code, 200)


## ============================================================================
## Helpers
## ============================================================================

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(logic))
    return tests


def new_user(self):
    self.user = User.objects.create(username='t1')
    self.user.set_password('t2')
    self.user.save()
