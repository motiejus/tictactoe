from django.contrib.auth.models import User

from tictactoelib.examples import player1



def qualification_bot(sender, **kwargs):
    from .models import Entry

    (q, created) = User.objects.get_or_create(username='Qualification-Bot')
    if Entry.objects.filter(user=q).first() is None:
        Entry.objects.create(user=q, code=player1)
