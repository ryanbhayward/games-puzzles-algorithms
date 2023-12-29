"""
  shared classes for games with rectangular boards, b/w/e/ cells
"""

from hexgo import Cell, Color, Game, IO, Pt, UF
from time import time

#################################################
class Stone_board:

  def print(self):
    IO.disp(self.game_type, IO.board_str(self.stones, self.n), self.r, self.c)

  def merge_blocks(self, p, q):
    print('merge blocks', p, q)
    proot, qroot = UF.union(self.parents, p, q)
    self.blocks[proot].update(self.blocks[qroot])
    self.liberties[proot].update(self.liberties[qroot])
    self.liberties[proot] -= self.blocks[proot]

  def remove_liberties(self, p, q): 
    proot = UF.find(self.parents, p)
    qroot = UF.find(self.parents, q)
    print('remove liberties from', proot)
    self.liberties[proot] -= self.blocks[qroot]
    self.liberties[qroot] -= self.blocks[proot]

  def add_stone(self, color, r, c):
    point, stns = Pt.rc_point(r, c, self.c), self.stones

    assert color in Cell.bw, 'invalid stone value'
    assert point not in stns[Cell.b].union(stns[Cell.w]), \
           'already a stone there'

    stns[color].add(point)
    self.blocks[point].add(point)

    for n in self.nbrs[point]:
      if n in self.stones[color]: # same-color nbr
        self.merge_blocks(n, point)
      if n in self.stones[Cell.opponent(color)]: # opponent nbr
        self.remove_liberties(n, point)

  def __init__(self, gt, rows, cols): 

    self.game_type = gt
    ### r horizontal lines, c vertical lines, r*c points
    self.r, self.c, self.n = rows, cols, rows * cols
    self.board_range = range(self.n) # board points
    self.stones = [set(), set()]  # start with empty board

    ### dictionairies
    self.nbrs      = {} # point -> neighbors
    self.blocks    = {} # point -> block
    self.liberties = {} # point -> liberties
    self.parents   = {} # point -> parents in block

    for point in range(self.n):
       self.nbrs[point]      = set()
       self.blocks[point]    = set()
       self.liberties[point] = set()
       self.parents[point]    = point

    print('\nparents of points\n')
    for p in range(self.n): 
      print(f'{p:2}', self.parents[p])
    Pt.show_point_names(self.game_type, self.r, self.c)

    for y in range(self.r):
      for x in range(self.c):
        p = Pt.rc_point(y, x, self.c)
        if x > 0: 
          self.nbrs[p].add( Pt.rc_point(y, x - 1, self.c) )
        if x < self.c - 1: 
          self.nbrs[p].add( Pt.rc_point(y, x + 1, self.c) )
        if y > 0: 
          self.nbrs[p].add( Pt.rc_point(y - 1, x, self.c) )
        if y < self.r - 1: 
          self.nbrs[p].add( Pt.rc_point(y + 1, x, self.c) )

    for p in range(self.n):
      self.liberties[p].update(self.nbrs[p])

################################ not using this yet
#class go_env:
#  def __init__(self, r, c):
#    self.board = go_board(r,c)
##################################################### 

