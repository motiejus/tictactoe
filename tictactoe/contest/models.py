from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from tictactoe.tools.validators import ByteLengthValidator
from tictactoe.tools.models import OwnManager

from . import fixtures

from .tasks import schedule_fight


class Entry(models.Model):
    _max_len = ByteLengthValidator(settings.MAX_CODE_SIZE)

    user = models.ForeignKey(User)
    code = models.TextField(validators=[_max_len])
    win = models.ManyToManyField(
        'self', symmetrical=False, related_name='loss',
        through='Fight')
    draw = models.ManyToManyField('self', through='Fight')

    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    own = OwnManager('user')

    @property
    def results(self):
        """Return dictionary (wins, draws, losses) of this entry.
        
        
        `draw` is non-symmetric, so we have to add the relationship backwards 
        as well."""
        return (self.win.count(), self.draw.count(), self.loss.count())

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
    e1 = models.ForeignKey(Entry)
    e2 = models.ForeignKey(Entry)

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


models.signals.post_migrate.connect(fixtures.qualification_bot)
