import logging

from django.core.serializers import serialize, deserialize
from django.conf import settings

from tictactoelib import compete

from tictactoe.celery_app import app

from .models import Fight, Entry, LatestEntry
from .logic import winner


logger = logging.getLogger(__name__)


def fight(e1, e2):
    logmsg = "Entry %d (%s) vs entry %d (%s) complete: %s, %s"
    e1log = e1.id, e1.user
    e2log = e2.id, e2.user

    kwargs = dict(
        cgroup=settings.FIGHT_CGROUP,
        memlimit=settings.FIGHT_MEMORY_LIMIT,
        timeout=settings.FIGHT_TIMEOUT,
    )
    round1 = compete(e1.code, e2.code, **kwargs)
    logger.debug(logmsg % (e1log + e2log + tuple(round1[:2])))

    round2 = compete(e2.code, e1.code, **kwargs)
    logger.debug(logmsg % (e2log + e1log + tuple(round2[:2])))

    Fight.from_compete(e1, e2, round1).save()
    Fight.from_compete(e2, e1, round2).save()
    return round1, round2


@app.task
def schedule_qualification(e1_json):
    e1 = next(deserialize('json', e1_json)).object
    args1 = e1.id, e1.user
    logger.debug("Executing qualification for entry %d (%s)" % args1)
    dumb = Entry.qualification_entry()
    round1, round2 = fight(e1, dumb)

    if winner(round1, round2) == 'e1':
        e1.add_latest()  # this entry is able to compete now
        # Schedule pvp
        les = LatestEntry.objects.exclude(user=e1.user).exclude(user=dumb)
        for latestentry in les.select_related('entry').all():
            e2 = latestentry.entry
            args2 = e1.id, e1.user, e2.id, e2.user
            logger.debug(("Scheduling competition between entries %d (%s) "
                          "and %d (%s)") % args2)
            e1_json = serialize('json', [e1])
            e2_json = serialize('json', [e2])
            schedule_compete.delay(e1_json, e2_json)
    else:
        logger.info("Entry %d (%s) did not qualify" % (e1.id, e1.user))


@app.task
def schedule_compete(e1_json, e2_json):
    e1 = next(deserialize('json', e1_json)).object
    e2 = next(deserialize('json', e2_json)).object
    fight(e1, e2)
