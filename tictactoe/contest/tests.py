import doctest
import itertools

try:
    from unittest import mock
except ImportError:  # python 3.2 or lower
    import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings

from tictactoe.contest import logic
from tictactoe.tools.testing import sync_celery

from .models import Entry, Fight
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


@sync_celery
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
        self.assertEqual(1, Entry.objects.count())
        self.client.post(reverse(views.upload), {'code': 'lua1'})
        self.assertEqual(2, Entry.objects.count())


class ResultsTestCase(TestCase):
    setUp = lambda self: new_user(self) or new_entry(self)

    def test_draw(self):
        Fight(x=self.e1, o=self.e2, result='draw').save()
        Fight(x=self.e2, o=self.e1, result='draw').save()
        self.assertEqual((0, 2, 0), self.e1.results)
        self.assertEqual((0, 2, 0), self.e2.results)

    def test_win_loss(self):
        Fight(x=self.e1, o=self.e2, result='win').save()
        self.assertEqual((1, 0, 0), self.e1.results)
        self.assertEqual((0, 0, 1), self.e2.results)


@sync_celery
class CeleryFightTestCase(TestCase):
    patch_x_wins = itertools.cycle((('ok', 'x', []), ('ok', 'o', [])))

    setUp = lambda self: new_user(self) or new_entry(self)

    def test_qualify(self):
        self.e1.qualify()
        self.assertEqual((0, 0, 2), self.e1.results)

    @mock.patch('tictactoe.contest.tasks.compete', side_effect=patch_x_wins)
    def test_two_users_draw(self, patch):
        self.e1.qualify()
        self.e2.qualify()
        # e2 qualified later, so won against qualification bot + e1
        self.assertEqual((4, 0, 0), self.e2.results)
        # e1 qualified earlier, so lost against e2
        self.assertEqual((2, 0, 2), self.e1.results)


# ============================================================================
# Helpers
# ============================================================================


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
    code1 = 'lua code'
    self.e1 = Entry.objects.create(user=self.user1, code=code1)
    self.e2 = Entry.objects.create(user=self.user2, code=code1)
