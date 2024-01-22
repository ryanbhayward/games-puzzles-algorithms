"""
  * simple set-based go environment    rbh 2024
  * similar to hex.py
  * they both use hexgo.py, stone_board.py
"""

from hexgo import Cell, Color, Game, IO, Pt, UF
from time import time
from stone_board import Stone_board

b,w = 0,1

m22demo = ((b,0,0),(w,0,1),(b,1,1),(w,1,0))
m34demo = ((b,2,1),(w,2,2),(b,1,1),(w,1,3),(b,1,2),(b,0,1))
m45demo = ((b,1,0),(w,1,2),(w,1,4),(w,0,3),(w,2,3),
           (b,3,0),(w,1,3),(b,2,1),(w,2,0),(b,3,3))
hw1 = ((b,2,1),(w,2,2),
       (b,1,2),(w,1,3),
       (b,1,1),(w,2,0),
       (b,0,0))

start_time = time()
gb = Stone_board(Game.go_game, 3, 4)

#for move in hw1:
#  gb.make_move(move)

for sort_nbrs in (True, False):
  gb.bfs_demo(0, sort_nbrs)
  gb.dfs_demo(0, sort_nbrs)

print('\ntime ', time() - start_time)
