"""Fight winner decision logic"""

__all__ = ['winner']


def error_to_win(r):
    """Change one's error to other's win"""

    if r == 'error1':
        return 'e2'
    elif r == 'error2':
        return 'e1'
    else:
        return r


def winner(r1, r2):
    """Return winner after two rounds

    >>> winner('e1', 'e1')
    'e1'
    >>> winner('e1', 'e2')
    'draw'
    >>> winner('e2', 'e1')
    'draw'
    >>> winner('e1', 'error1')
    'draw'
    >>> winner('e1', 'error2')
    'e1'
    >>> winner('error1', 'error2')
    'draw'
    >>> winner('error2', 'error1')
    'draw'
    >>> winner('error1', 'error1')
    'e2'
    >>> winner('draw', 'draw')
    'draw'
    >>> winner('draw', 'e1')
    'e1'
    >>> winner('draw', 'error1')
    'e2'
    """
    r1 = error_to_win(r1)
    r2 = error_to_win(r2)

    # No errors from this point, only 'draw', 'e1' or 'e2'
    if r1 == r2:  # both rounds same won or both draw
        return r1
    elif r1.startswith('e') and r2.startswith('e'):  # both won
        return 'draw'

    # One draw, the other won. Pick the winner.
    return r1 == 'draw' and r2 or r1
