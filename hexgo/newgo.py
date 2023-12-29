"""
  * simple go environment    rbh 2024
    trying to use Stone_board
"""

from hexgo import Cell, Color, Game, IO, Pt, UF
from time import time
from stone_board import Stone_board


m22demo = ((0,0,0),(1,0,1),(0,1,1),(1,1,0))
m45demo = ((0,1,0),(1,1,2),(1,1,4),(1,0,3),(1,2,3), \
           (0,3,0),(1,1,3),(0,2,1),(1,2,0),(0,3,3))

start_time = time()

gb = Stone_board(Game.go_game, 6, 6)
for move in m45demo:
#gb = go_board(2,2)
#for move in m22demo:
  gb.add_stone(move[0], move[1], move[2])
  gb.print()
IO.show_blocks(gb.n, gb.stones, gb.parents, gb.blocks, gb.liberties)

end_time = time()
print('time ', end_time - start_time)
