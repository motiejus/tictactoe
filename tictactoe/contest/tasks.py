#from tictactoelib.headless_run import compete
#from tictactoelib.examples import player1

from tictactoe.celery_app import app


@app.task
def schedule_qualifying(e1):
    round1 = compete(e1.code, player1)
    if round1 == 'e2':
        return
    round2 = compete(player1, e1.code)


@app.task
def schedule_fight(e1, e2):
    schedule_draw_fight(e1, e2)


@app.task
def schedule_draw_fight(e1, e2):
    from tictactoe.contest.models import Fight
    f = Fight(e1=e1, e2=e2, round1='draw', round2='draw')
    f.save()
