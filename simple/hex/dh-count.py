#!/usr/bin/env python

# upper bound on number of dark hex strategies   rbh 2021

# abrupt dark hex:
#     state(n,h): n unknown-status cells, h opponent-hidden stones
#     player makes move
#     if occupied, opponent stone there: 
#         now state(n-1, h-1)
#         after opponent move
#     if unoccupied, player stone there:
#         now state(n-1, h)


Adh-vals = dict()

def adh(n, h): # number of strategies, n unknown cells, h opponent cells
    if (n <= 0 or n <= h): return 0
    

#  damn, trickier than I thought, because we don't know
#  how many times the opponent has crashed,
#  worst case, we assume opponent crashes max number of times,
#  but we should also assume that the opponent
#  never tries the same cell more than once
