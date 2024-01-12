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
m34demo = ((0,2,1),(1,2,2),(0,1,1),(1,1,3),(0,1,2))
m45demo = ((0,1,0),(1,1,2),(1,1,4),(1,0,3),(1,2,3), \
           (0,3,0),(1,1,3),(0,2,1),(1,2,0),(0,3,3))

start_time = time()

gb = Stone_board(Game.go_game, 3, 4)
IO.show_blocks(gb.p_range, gb.n, gb.stones, gb.parents, gb.blocks, gb.liberties)
for move in m34demo:
  gb.add_stone(move[0], Pt.rc_point(move[1], move[2], gb.c))
  IO.show_pairs('point parents', gb.parents)
  gb.print()
IO.show_blocks(gb.p_range, gb.n, gb.stones, gb.parents, gb.blocks, gb.liberties)

end_time = time()
print('time ', end_time - start_time)
