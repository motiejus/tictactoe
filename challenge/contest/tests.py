import doctest

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

from challenge.contest import logic

from .forms import CodeUploadForm
from .models import Entry



class EntryTestCase(TestCase):
    setUp = lambda self: new_user(self)

    def test_code_constraint(self):
        """ 'š' is a 2-byte utf8 character"""
        code = "".join(['š'] * (settings.MAX_CODE_SIZE + 1)).encode('utf8')
        e = Entry.objects.create(user=self.user, code=code)
        self.assertRaises(ValidationError, e.full_clean)


class ViewTestCase(TestCase):
    def test_index(self):
        request = self.client.get('/')
        self.assertEqual(request.status_code, 200)

class UploadTestCase(TestCase):
    setUp = lambda self: new_user(self)

    def test_upload_toobig(self):
        """Try to put a big source file with lots of unicode characters"""


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
