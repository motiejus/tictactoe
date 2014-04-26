import logging

from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import date, filesizeformat as fmt
from django.conf import settings

from tictactoe.tools.validators import ByteLengthValidator
from tictactoe.tools.models import OwnManager

from . import fixtures


logger = logging.getLogger(__name__)


class HandedOutCaps(models.Model):
    user = models.ForeignKey(User)
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "To %s at %s" % (self.user, date(self.when, "Y-m-d H:i:s"))

    class Meta:
        ordering = 'when',


class Entry(models.Model):
    _max_len = ByteLengthValidator(settings.MAX_CODE_SIZE)

    user = models.ForeignKey(User)
    code = models.TextField(validators=[_max_len])

    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    own = OwnManager('user')

    @property
    def codesize(self):
        return len(self.code.encode('utf8'))

    def get_absolute_url(self):
        return reverse_lazy('tictactoe.contest.views.entry', args=[self.id])

    def __str__(self):
        return "<Entry %d by %s (%s)>" % (
            self.id, self.user, fmt(self.codesize))

    def add_latest(self):
        """After qualifying, make it LatestEntry of this user"""
        latest = LatestEntry.objects.filter(user=self.user).first()
        if latest is None:
            LatestEntry(user=self.user, entry=self).save()
        else:
            latest.entry = self
            latest.save()

    def qualify(self):
        """Scheulde a qualification with dumb_player and maybe go compete"""
        from .tasks import schedule_qualification
        logger.info("Scheduling %s for qualification" % self)
        schedule_qualification.delay(serialize('json', [self]))

    @staticmethod
    def qualification_entry():
        u = User.objects.get(username='Qualification-Bot')
        return Entry.objects.get(user=u)

    class Meta:
        verbose_name_plural = 'Entries'
        ordering = '-uploaded',


class LatestEntry(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)

    def calc_results(self):
        r1 = Fight.objects.filter(
            x__latestentry=self, o__latestentry__isnull=False
            ).values('result').annotate(cnt=models.Count('result'))
        r2 = Fight.objects.filter(
            o__latestentry=self, x__latestentry__isnull=False
            ).values('result').annotate(cnt=models.Count('result'))
        d1 = dict(((d['result'], d['cnt']) for d in r1))
        d2 = dict(((d['result'], d['cnt']) for d in r2))
        win = d1.get('win', 0) + d2.get('loss', 0)
        draw = d1.get('draw', 0) + d2.get('draw', 0)
        loss = d1.get('loss', 0) + d2.get('win', 0)
        return win, draw, loss

    def __str__(self):
        return "<LatestEntry by %s>" % (self.user)

    class Meta:
        verbose_name_plural = 'Latest Entries'


class Fight(models.Model):
    """e1 is x, e2 is o. Results relative to e1.

    Each Entry has two Fight objects: one with x, one with o"""

    FIGHT_RESULT = (
        ('win', _('win')),
        ('draw', _('draw')),
        ('loss', _('loss')),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
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

    def result_of_x(self):
        return self.result

    def result_of_o(self):
        if self.result == 'draw':
            return 'draw'
        return self.result == 'loss' and 'win' or 'win'

    class Meta:
        index_together = (
            ('x', 'result'),
            ('o', 'result'),
        )
        unique_together = ('x', 'o')

    @staticmethod
    def from_compete(x, o, round_result):
        """Creates Fight instance from output of tictactoelib.compete"""
        fight, _created = Fight.objects.get_or_create(x=x, o=o)
        if round_result[0] == 'ok':
            _, xodraw, gameplay = round_result
            res = 'draw'
            if xodraw == 'x' or xodraw == 'o':
                res = xodraw == 'x' and 'win' or 'loss'
            fight.gameplay = gameplay
            fight.result = res
            return fight
        elif round_result[0] == 'error':
            _, xo, reason, gameplay = round_result
            res = 'win' if xo == 'o' else 'loss'
            fight.gameplay = gameplay
            fight.error = reason
            fight.result = res
            return fight

    def get_absolute_url(self):
        return reverse_lazy('tictactoe.contest.views.fight', args=[self.id])

    def __str__(self):
        return "<Fight %s vs %s. Result: %s>" % (self.x, self.o, self.result)


models.signals.post_migrate.connect(fixtures.qualification_bot)
