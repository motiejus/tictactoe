import doctest

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings

from challenge.contest import logic

from .models import Entry
from . import views


class EntryTestCase(TestCase):
    setUp = lambda self: new_user(self)

    def test_code_constraint_over(self):
        """code less than allowed chars, more than allowed bytes"""
        # 'š' is a 2-byte utf8 character
        code = "".join(['š'] * (settings.MAX_CODE_SIZE // 2 + 1))
        e = Entry.objects.create(user=self.user1, code=code)
        self.assertRaises(ValidationError, e.full_clean)

    def test_code_constraint_just_enough(self):
        # 'š' is a 2-byte utf8 character
        code = "".join(['š'] * (settings.MAX_CODE_SIZE // 2))
        e = Entry.objects.create(user=self.user1, code=code)
        self.assertIsNone(e.full_clean())

    def test_code_size(self):
        code = 'žžž'
        e = Entry.objects.create(user=self.user1, code=code)
        self.assertEqual(6, e.codesize)


class ViewTestCase(TestCase):
    setUp = lambda self: new_user(self)

    def test_index(self):
        request = self.client.get('/')
        self.assertEqual(request.status_code, 200)

    def test_upload_get(self):
        self.client.login(username='u1', password='u1')
        response = self.client.get(reverse(views.upload))
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        self.assertTrue(self.client.login(username='u1', password='u1'))
        self.assertEqual(0, Entry.objects.count())
        self.client.post(reverse(views.upload), {'code': 'lua1'})
        self.assertEqual(1, Entry.objects.count())

class ResultsTestCase(TestCase):
    setUp = lambda self: new_user(self)


## ============================================================================
## Helpers
## ============================================================================


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(logic))
    return tests


def new_user(self):
    self.user1 = User.objects.create(username='u1')
    self.user1.set_password('u1')
    self.user1.save()
    self.user2 = User.objects.create(username='u2')
    self.user2.set_password('u2')
    self.user2.save()
