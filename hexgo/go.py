"""
  * simple set-based go environment    rbh 2024
  * similar to hex.py
  * they both use hexgo.py, stone_board.py
"""

from hexgo import Cell, Color, Game, IO, Pt, UF
from time import time
from stone_board import Stone_board


m22demo = ((0,0,0),(1,0,1),(0,1,1),(1,1,0))
# 1.b b3  2.w c3 ...
#m34demo = ((0,2,1),(1,2,2),(0,1,2),(1,1,3),(0,1,1))
m34demo = ((0,2,1),(1,2,2),(0,1,1),(1,1,3),(0,1,2),(0,0,1))
m45demo = ((0,1,0),(1,1,2),(1,1,4),(1,0,3),(1,2,3), \
           (0,3,0),(1,1,3),(0,2,1),(1,2,0),(0,3,3))

start_time = time()
gb = Stone_board(Game.go_game, 3, 4)

for move in m34demo:
  gb.make_move(move)

print('time ', time() - start_time)
