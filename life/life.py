#!/usr/bin/env python3

"""
Conway's game of life, infinite grid    RBH 2020
"""

from time import sleep
import sys
from paint import paint

PTS = '.*#'
DEAD, ALIVE, GUARD = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[GUARD]

pause = .2

"""
replace char-in-string
"""


def change_str(s, where, what):
    return s[:where] + what + s[where+1:]


"""
board functions
  * represent board as string in row-major order 
  * cell's point is 1-d string index
  * cell's coordinate is 2-d row/column indices
"""


def point(r, c, cols):
    return c + r*cols


def coord(p, cols):
    return divmod(p, cols)


def live_row(r, B, cols):
    return ACH in B[point(r, 1, cols): point(r, cols, cols)]


def live_col(c, B, cols):
    n, pt = len(B), point(1, c, cols)
    while pt < n:
        if B[pt] == ACH:
            return True
        pt += cols
    return False


def alphanum(p, C):  # for showing coordinates
    r, c = coord(p, C)
    return 'abcdefghj'[c] + '1234566789'[r]


def get_board():
    B = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            B.append(line.rstrip().replace(' ', ''))
        rows, cols = len(B), len(B[0])
        for j in range(1, rows):
            assert(len(B[j]) == cols)
        return B, rows, cols


def pad(B, r, c):
    '''

    to avoid boundary collisions,
    ensure B has empty first/last row/column
    by if necessary adding empty first/last row/column
    :param B: [description]
    :type B: [type]
    :param r: [description]
    :type r: [type]
    :param c: [description]
    :type c: [type]
    :returns: [description]
    :rtype: {[type]}
    '''
    assert(len(B) == r*c+1)  # this board is already padded
    if live_row(r-2, B, c):  # last non-guard row
        B = B[0: point(r-1, 1, c)] + DCH*(c-1) + GCH*(c+1)
        r += 1
    if live_row(1, B, c):  # first non-guard row
        B = GCH*c + GCH + DCH*(c-1) + B[point(1, 0, c): 1+r*c]
        r += 1
    if live_col(c-1, B, c):  # last column
        new = GCH*(c+1)
        for j in range(1, r-1):
            new += B[point(j, 0, c): point(j, c, c)] + DCH
        B = new + GCH*(c+2)
        c += 1
    if live_col(1, B, c):  # first non-guard column
        new = GCH*(c+1)
        for j in range(1, r-1):
            new += GCH + DCH + B[point(j, 1, c): point(j, c, c)]
        B = new + GCH*(c+2)
        c += 1
    return B, r, c


def add_guards(B, r, c):
    '''
    add guards: top row, left column, bottom row (with one extra)
    original board        guarded board
                             GGGG
      .x.                    G.x.
      ..x                    G..x
      xxx                    Gxxx
      ...                    G...
                             GGGGG  <- don't forget last guard
    [description]
    :param B: [description]
    :type B: [type]
    :param r: [description]
    :type r: [type]
    :param c: [description]
    :type c: [type]
    '''
    B.insert(0, GCH * (1 + c))
    for j in range(r):
        B[j+1] = GCH + B[j+1]
    B.append(GCH * (2 + c))
    return(''.join(B), len(B), len(B[0]))


def showboard(board, row, C, gap, pause):
    # add numeric row indices, alphabetic column indices
    pretty = '\n    '
    if C <= 26:
        for c in range(C):  # columns
            pretty += gap + paint(chr(ord('a')+c), PTS)
    else:
        gap = ''

    pretty += '\n'
    for j in range(row):  # rows
        if j < 10:
            pretty += ' '
        pretty += gap + paint(str(j), PTS) + ' '
        for k in range(C):  # columns
            pretty += gap + paint([board[point(j, k, C)]], PTS)
        if j == row-1:  # in last row, put last guard
            pretty += gap + paint(board[row*C], PTS)
        pretty += '\n'
    print(pretty)
    sleep(pause)


""" 
Conway's next-state formula
"""


def num_nbrs(s, j, cols, ch):
    # state, cell, columns, nbr-type
    num = 0
    if s[j-(cols+1)] == ch:
        num += 1
    if s[j - cols] == ch:
        num += 1
    if s[j-(cols-1)] == ch:
        num += 1
    if s[j-1] == ch:
        num += 1
    if s[j+1] == ch:
        num += 1
    if s[j+(cols-1)] == ch:
        num += 1
    if s[j + cols] == ch:
        num += 1
    if s[j + cols+1] == ch:
        num += 1
    return num


def next_state(s, cols):
    new = ''
    for j in range(len(s)):
        ch = s[j]
        if ch == GCH:
            new += GCH
        else:
            m = num_nbrs(s, j, cols, ACH)
            if ch == ACH:
                new += ACH if m > 1 and m < 4 else DCH
            else:
                new += ACH if m == 3 else DCH
    return new


def interact(max_itn):
    """
    input, output
    """
    itn = 0
    B, r, c = get_board()
    B, r, c = add_guards(B, r, c)
    while itn <= max_itn:
        B, r, c = pad(B, r, c)
        newB = next_state(B, c)
        if newB == B:
            break
        if r <= 10000:
            showboard(B, r, c, ' ', pause)
        itn += 1
        B = newB
    showboard(B, r, c, ' ', pause)
    print('iterations', itn)


def main():
    interact(1200)


if __name__ == '__main__':
    main()
