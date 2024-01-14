"""
  * simple set-based hex environment    rbh 2024
  * similar to go.py
  * they both use hexgo.py, stone_board.py
"""
#   ideas from ...
#     * Michi (by Petr Baudis)
#     * Morat (by Timo Ewalds)
#     * Miaowy (by rbh)
#     * Benzene (by 
#         Broderick Arneson, Philip Henderson, Jakub Pawlewicz,
#         Aja Huang, Yngvi Bjornsson, Michael Johanson, Morgan Kan,
#         Kenny Young, Noah Weninger, Chao Gao, rbh)
#     * hex (by Luke Schultz)
#     * hsearch (by Owen Randall)

#from copy import deepcopy
#from random import shuffle, choice
#import math

from hexgo import Cell, Color, Game, IO, Pt, UF
from stone_board import Stone_board
from time import time

#mdemo =   ((0,0,1),(0,1,0))
#m22demo = ((0,0,0),(1,0,1),(0,1,1),(1,1,0))
#m45demo = ((0,1,0),(1,1,2),(1,1,4),(1,0,3),(1,2,3),\
#           (0,3,0),(1,1,3),(0,2,1),(1,2,0),(0,3,3))
m33demo  = ((0,1,1),(1,0,0),(0,2,1),(1,2,2),(0,0,1))
m33tdemo  = ((1,1,1),(0,0,0),(1,0,2),(0,2,2),(1,2,0))


start_time = time()
win_msg = ' ! ! ! game over '

hb = Stone_board(Game.hex_game, 3, 3)
hb.show_blocks()

for move in m33demo:
  hb.add_stone(move[0], Pt.rc_point(move[1], move[2], hb.c))
  hb.print()
  hb.show_blocks()
  hb.show_parents()
  if hb.hex_win(Cell.b): print(win_msg, 'black wins')
  if hb.hex_win(Cell.w): print(win_msg, 'white wins')

end_time = time()
print('time ', end_time - start_time)
