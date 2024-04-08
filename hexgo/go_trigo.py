"""
  * simple set-based go environment    rbh 2024
"""

from hexgo_trigo import Cell, Color, IO, Pt, UF
from time import time
from stone_trigo import Stone_board

b,w = 0,1

start_time = time()
gb = Stone_board()

#for move in hw1:
#  gb.make_move(move)

for sort_nbrs in (True, False):
  gb.bfs_demo(2, sort_nbrs)
  gb.dfs_demo(2, sort_nbrs, True)
  gb.dfs_demo(2, sort_nbrs, False)

print('\ntime ', time() - start_time)
