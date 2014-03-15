from challenge.celery_app import app


@app.task
def schedule_fight(e1, e2):
    schedule_draw_fight(e1, e2)


@app.task
def schedule_draw_fight(e1, e2):
    from challenge.contest.models import Fight
    f = Fight(e1=e1, e2=e2, round1='draw', round2='draw')
    f.save()
