from tictactoelib import compete

from tictactoe.celery_app import app

from .models import Fight, Entry
# from .logic import winner


@app.task
def schedule_qualification(e1):
    dumb = Entry.qualification_entry()
    round1 = compete(e1.code, dumb.code)
    round2 = compete(dumb.code, e1.code)

    fight1 = Fight.from_compete(e1, dumb, round1)
    fight2 = Fight.from_compete(dumb, e1, round2)

    fight1.save()
    fight2.save()
