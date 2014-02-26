from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .logic import winner


class Entry(models.Model):
    user = models.ForeignKey(User)
    code = models.TextField(max_length=60000)
    fights = models.ManyToManyField(
        'Entry', symmetrical=False, through='Fight')


class LatestEntry(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)


class Fight(models.Model):
    """Encapsulates fight between two entries. Results of 2 rounds.

    Round1: e1 = x, e2 = o;
    Round2: e1 = o, e2 = x

    Returns: 'e1', 'e2', 'draw'
    """
    FIGHT_RESULTS = (
        ('e1', _("Entry 1 won")),
        ('e2', _("Entry 2 won")),
        ('draw', _("Draw")),
        ('Error', (
            ('error_1', _("Error by Entry 1")),
            ('error_2', _("Error by Entry 2"))))
    )

    e1 = models.ForeignKey(Entry, related_name='+')
    e2 = models.ForeignKey(Entry, related_name='+')
    round1 = models.CharField(max_length=16, choices=FIGHT_RESULTS)
    round2 = models.CharField(max_length=16, choices=FIGHT_RESULTS)

    class Meta:
        unique_together = ('e1', 'e2')

    def winner(self):
        return winner(self.r1, self.r2)
