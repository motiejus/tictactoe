from tictactoelib import compete
from tictactoelib.examples import dumb_player

from tictactoe.celery_app import app


@app.task
def schedule_qualification(e1):
    round1 = compete(e1.code, dumb_player)
    round2 = compete(dumb_player, e1.code)
    print(round1, round2)
