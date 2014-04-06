"""Fight winner decision logic"""

__all__ = ['winner']


def flip(res):
    """flips 'x', 'o' or 'draw'."""
    if res == 'x':
        return 'o'
    elif res == 'o':
        return 'x'
    elif res == 'draw':
        return 'draw'
    else:
        raise RuntimeError("Invalid res: %s" % str(res))


def error_to_win(r):
    """Change one's error to other's win"""
    flip = lambda c: c == 'x' and 'o' or 'x'
    if r[0] == 'error':
        return flip(r[1])
    elif r[0] == 'ok':
        return r[1]
    else:
        raise RuntimeError("Invalid r[0]: %s", str(r[0]))


def winner(r1, r2):
    """Return winner of two rounds: 'e1' or 'e2' or 'draw'.

    round1 is e1 (x) vs e2 (o). round2 is e2(x) vs e1(o).

    Input format of r1 and r2:
    * 'ok', 'x' | 'draw' | 'o', ...
    * 'error', 'x' | 'o', ...

    >>> okx = 'ok', 'x'
    >>> oko = 'ok', 'o'
    >>> okdraw = 'ok', 'draw'
    >>> errx = 'error', 'x'
    >>> erro = 'error', 'o'

    >>> winner(okx, oko)
    'e1'
    >>> winner(okx, okx)
    'draw'
    >>> winner(oko, oko)
    'draw'
    >>> winner(okx, erro)
    'draw'
    >>> winner(okx, errx)
    'e1'
    >>> winner(errx, errx)
    'draw'
    >>> winner(erro, erro)
    'draw'
    >>> winner(errx, erro)
    'e2'
    >>> winner(okdraw, okdraw)
    'draw'
    >>> winner(okdraw, oko)
    'e1'
    >>> winner(okdraw, erro)
    'e2'
    """

    f1 = error_to_win(r1)
    f2 = error_to_win(r2)

    return {
        ('x', 'o'): 'e1',
        ('o', 'x'): 'e2',

        ('draw', 'o'): 'e1',
        ('o', 'draw'): 'e2',

        ('draw', 'x'): 'e2',
        ('x', 'draw'): 'e1',

        ('x', 'x'): 'draw',
        ('o', 'o'): 'draw',
        ('draw', 'draw'): 'draw',
        }[(f1, f2)]
