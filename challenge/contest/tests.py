import doctest

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings

from challenge.contest import logic
from challenge.tools.testing import sync_celery

from .models import Entry, LatestEntry, Fight
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
    setUp = lambda self: new_user(self) or new_entry(self)

    def test_draw(self):
        Fight(e1=self.e1, e2=self.e2, round1='draw', round2='draw').save()
        self.assertEqual({'win': 0, 'draw': 1, 'loss': 0}, self.e1.results)
        self.assertEqual({'win': 0, 'draw': 1, 'loss': 0}, self.e2.results)

    def test_win_loss(self):
        Fight(e1=self.e1, e2=self.e2, round1='e1', round2='draw').save()
        self.assertEqual({'win': 1, 'draw': 0, 'loss': 0}, self.e1.results)
        self.assertEqual({'win': 0, 'draw': 0, 'loss': 1}, self.e2.results)


@sync_celery
class CeleryFightTestCase(TestCase):
    setUp = lambda self: new_user(self) or new_entry(self)

    def test_two_users_draw(self):
        self.e2.compete()
        self.assertEqual(1, Fight.objects.count())


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


def new_entry(self):
    code = 'lua code'
    self.e1 = Entry.objects.create(user=self.user1, code=code)
    self.e1.save()
    self.assertEqual(1, LatestEntry.objects.count())
    self.e2 = Entry.objects.create(user=self.user2, code=code)
    self.e2.save()
    self.assertEqual(2, LatestEntry.objects.count())
