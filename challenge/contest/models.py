from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from challenge.tools.validators import ByteLengthValidator
from challenge.tools.models import OwnManager

from .logic import winner
from .tasks import schedule_fight


class Entry(models.Model):
    _max_len = ByteLengthValidator(settings.MAX_CODE_SIZE)

    user = models.ForeignKey(User)
    code = models.TextField(validators=[_max_len])
    fights = models.ManyToManyField('Fight', symmetrical=False, blank=True)

    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    own = OwnManager('user')

    @property
    def results(self):
        """Return dictionary (wins, draws, losses) of this entry"""
        if hasattr(self, '_results'):
            return self._results
        flip = lambda e: 'e2' if e == 'e1' else 'e1'
        win, draw, loss = 0, 0, 0
        for e in 'e1', 'e2':
            for fight in Fight.objects.filter(**{e: self}):
                if fight.winner == e:
                    win += 1
                elif fight.winner == flip(e):
                    loss += 1
                elif fight.winner == 'draw':
                    draw += 1
                else:
                    assert False, "bad winner"
        self._results = {'win': win, 'draw': draw, 'loss': loss}
        return self._results

    @property
    def codesize(self):
        return len(self.code.encode('utf8'))

    def get_absolute_url(self):
        return reverse_lazy('challenge.contest.views.entry', args=[self.id])

    def __str__(self):
        return "<Entry by %s (%d bytes)>" % (self.user, self.codesize)

    @staticmethod
    def add_latest(sender, instance, created, **kwargs):
        """After saving Entry instance, make it LatestEntry of this user"""
        latest = LatestEntry.objects.filter(user=instance.user).first()
        if latest is None:
            LatestEntry(user=instance.user, entry=instance).save()
        else:
            latest.entry = instance
            latest.save()

    def compete(self):
        """Compete with all LatestEntries of non-current user.

        Schedules a few tasks for celery
        """
        latest_entries = LatestEntry.objects.exclude(user=self.user).all()
        for entry in (e.entry for e in latest_entries):
            schedule_fight.delay(self, entry)


models.signals.post_save.connect(Entry.add_latest, sender=Entry)


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

    @property
    def winner(self):
        """Returns: 'e1', 'e2', 'draw'"""
        return winner(self.round1, self.round2)
