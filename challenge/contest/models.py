from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .logic import winner


class Entry(models.Model):
    user = models.ForeignKey(User)
    code = models.TextField(max_length=settings.MAX_CODE_SIZE)
    fights = models.ManyToManyField(
        'Entry', symmetrical=False, through='Fight', blank=True)

    def clean(self):
        sz, _max = len(self.code.encode('utf8')), settings.MAX_CODE_SIZE
        if sz > _max:
            err = "Code is %d bytes long, must be <= %d" % (sz, _max)
            raise ValidationError(err)


class LatestEntry(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)


class Fight(models.Model):
    """Encapsulates fight between two entries. Results of 2 rounds.

    Round1: e1 = x, e2 = o;
    Round2: e1 = o, e2 = x
    """
    FIGHT_RESULTS = (
        ('e1', _("Entry 1 won")),
        ('e2', _("Entry 2 won")),
        ('draw', _("Draw")),
        ('Error', (
            ('error1', _("Error by Entry 1")),
            ('error2', _("Error by Entry 2"))))
    )

    e1 = models.ForeignKey(Entry, related_name='+')
    e2 = models.ForeignKey(Entry, related_name='+')
    round1 = models.CharField(max_length=16, choices=FIGHT_RESULTS)
    round2 = models.CharField(max_length=16, choices=FIGHT_RESULTS)

    class Meta:
        unique_together = ('e1', 'e2')

    def winner(self):
        """Returns: 'e1', 'e2', 'draw'"""
        return winner(self.r1, self.r2)
