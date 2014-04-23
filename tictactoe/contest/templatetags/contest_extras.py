from django import template

register = template.Library()


@register.filter
def result_of(fight, user):
    """Returns result of a fight relative to the user.

    So this:

        User {{ entry.user }}
            {% if fight.x.user == entry.user %}
                {{ fight.result_of_x }}
            {% else %}
                {{ fight.result_of_o }}
            {% endif %}
        the match!

    Can be replaced by:

        User {{ entry.user }} {{ fight|result_of:entry.user }} the match!

    >>> from tictactoe.contest.models import Fight
    >>> result_of(Fight(x=e1, o=e2, result='win'), user1)
    'win'
    >>> result_of(Fight(x=e1, o=e2, result='win'), user2)
    'loss'
    >>> result_of(Fight(x=e1, o=e2, result='loss'), user1)
    'loss'
    >>> result_of(Fight(x=e1, o=e2, result='loss'), user2)
    'win'
    >>> result_of(Fight(x=e1, o=e2, result='draw'), user1)
    'draw'
    >>> result_of(Fight(x=e1, o=e2, result='draw'), user2)
    'draw'
    """
    if fight.x.user == user:
        return fight.result
    else:
        if fight.result == 'draw':
            return 'draw'
        return fight.result == 'loss' and 'win' or 'loss'
