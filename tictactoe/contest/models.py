from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from tictactoe.tools.validators import ByteLengthValidator
from tictactoe.tools.models import OwnManager

from . import fixtures


class Entry(models.Model):
    _max_len = ByteLengthValidator(settings.MAX_CODE_SIZE)

    user = models.ForeignKey(User)
    code = models.TextField(validators=[_max_len])

    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    own = OwnManager('user')

    @property
    def results(self):
        """Return dictionary (wins, draws, losses) of this entry.

        TODO: rewrite to ORM/SQL in the future?"""
        r1 = Fight.objects.filter(x=self).values_list('result', flat=True)
        r2 = Fight.objects.filter(o=self).values_list('result', flat=True)
        wins = [1 for r in r1 if r == 'win'] + [1 for r in r2 if r == 'loss']
        lose = [1 for r in r1 if r == 'loss'] + [1 for r in r2 if r == 'win']
        draw = [1 for r in r1 if r == 'draw'] + [1 for r in r2 if r == 'draw']
        return sum(wins), sum(draw), sum(lose)

    @property
    def codesize(self):
        return len(self.code.encode('utf8'))

    def get_absolute_url(self):
        return reverse_lazy('tictactoe.contest.views.entry', args=[self.id])

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

    def qualify(self):
        """Scheulde a qualification with example dumb_player"""
        from .tasks import schedule_qualification
        schedule_qualification.delay(serialize('json', [self]))

    @staticmethod
    def qualification_entry():
        u = User.objects.get(username='Qualification-Bot')
        return Entry.objects.get(user=u)


models.signals.post_save.connect(Entry.add_latest, sender=Entry)


class LatestEntry(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)


class Fight(models.Model):
    """e1 is x, e2 is o. Results relative to e1.

    Each Entry has two Fight objects: one with x, one with o"""

    FIGHT_RESULT = (
        ('win', _('win')),
        ('draw', _('draw')),
        ('loss', _('loss')),
    )

    x = models.ForeignKey(Entry, related_name='e1')
    o = models.ForeignKey(Entry, related_name='e2')

    # len(",".join(map(str, range(1, 81)))) == 230
    # Zero signifies error and in case of error is always the last number
    gameplay = models.CommaSeparatedIntegerField(
        max_length=230,
        help_text=_(
            "Gameplay flow. Board is separated to 81 cells. Each "
            "number means a move by alternating player. For example, "
            "'10,1,0' means: x placed (2,1,1,1), o placed (1,1,1,1) and "
            "x made an error. In case 0 is at the end (like in the example), "
            "'error' field is non-empty.")
    )

    error = models.CharField(
        max_length=255, blank=True,
        help_text=_("Non-empty if `gameplay' ends with zero")
    )

    result = models.CharField(
        max_length=10, choices=FIGHT_RESULT,
        help_text=_("Fight result of x (e1) versus o (e2). Relative to e1.")
    )

    class Meta:
        index_together = (
            ('x', 'result'),
            ('o', 'result'),
        )

    @staticmethod
    def from_compete(x, o, round_result):
        """Creates Fight instance from output of tictactoelib.compete"""
        if round_result[0] == 'ok':
            _, xodraw, gameplay = round_result
            res = 'draw'
            if xodraw == 'x' or xodraw == 'o':
                res = xodraw
            return Fight(x=x, o=o, gameplay=gameplay, result=res)
        elif round_result[0] == 'error':
            _, xo, reason, gameplay = round_result
            res = 'win' if xo == 'o' else 'loss'
            return Fight(x=x, o=o, gameplay=gameplay, error=reason, result=res)

    def __str__(self):
        return "<Fight %s vs %s. Result: %s>" % (self.x, self.o, self.result)


models.signals.post_migrate.connect(fixtures.qualification_bot)
