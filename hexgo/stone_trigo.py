"""
  shared classes for games with rectangular boards, b/w/e/ cells
"""

from hexgo_trigo import Cell, Color, IO, Pt, UF
from time import time

#################################################
class Stone_board:

  def print(self):
    IO.disp(self.game_type, IO.board_str(self.stones, self.n), self.r, self.c)

  def merge_blocks(self, p, q):
    print('union blocks', p, q)
    proot, qroot = UF.union(self.parents, p, q)
    self.blocks[proot].update(self.blocks[qroot])
    self.liberties[proot].update(self.liberties[qroot])
    self.liberties[proot] -= self.blocks[proot]

  def remove_liberties(self, p, q): 
    proot = UF.find(self.parents, p)
    qroot = UF.find(self.parents, q)
    #print('remove liberties from', proot)
    self.liberties[proot] -= self.blocks[qroot]
    self.liberties[qroot] -= self.blocks[proot]

  def add_stone(self, color, point):
    print('\n-------------\nadd_stone', Cell.io_ch[color], point)
    assert color in Cell.bw, 'invalid stone value'
    assert point not in self.stones[Cell.b] and \
           point not in self.stones[Cell.w], 'already a stone there'
    self.stones[color].add(point)
    self.blocks[point].add(point)

    for n in self.nbrs[point]:
      if n in self.stones[color]: # same-color nbr
        self.merge_blocks(n, point)
      if n in self.stones[Cell.opponent(color)]: # opponent nbr
        self.remove_liberties(n, point)

  def make_move(self, move):
    self.add_stone(move[0], Pt.rc_point(move[1], move[2], self.c))
    self.show_blocks()
    self.show_parents()
    if self.hex_win(Cell.b): print('!!! game over: black wins')
    if self.hex_win(Cell.w): print('!!! game over: white wins')
    #self.print()

  def hex_win(self, cell_color):
     if self.game_type != Game.hex_game: 
         return False
     if cell_color == Cell.b:
       return UF.in_same_block(self.parents, self.top, self.btm)
     return UF.in_same_block(self.parents, self.lft, self.rgt)

  def show_parents(self):
    print('parents ',end='')
    for x in self.parents: 
      if x != self.parents[x]:
        print(x, ' ', self.parents[x], sep='', end='  ')
    print()

  def show_liberties(self):
    print('liberties ',end='')
    for p in self.p_range:
      print(p, self.liberties[p])
    print()


  def show_blocks(self):
    for pcol in Cell.bw:
      print(Cell.io_ch[pcol], 'blocks', end=' ')
      for p in self.p_range:
        if Pt.point_color(self.stones, p) == pcol and \
           UF.is_root(self.parents, p):
          print(p, self.blocks[p], end=' ')
      print()
      print(Cell.io_ch[pcol], 'liberties', end=' ')
      for p in self.p_range:
        if Pt.point_color(self.stones, p) == pcol and \
           UF.is_root(self.parents, p):
          print(p, self.liberties[p], end=' ')
      print()

  def dfs(self, p, seen, sort_nbrs, pre_order): # p is cell in hex, point in go
    if not seen[p]:
      if pre_order: print(p, end=' ')
      seen[p] = True
      for nbr in sorted(self.nbrs[p]) if sort_nbrs else self.nbrs[p]:
        self.dfs(nbr, seen, sort_nbrs, pre_order)
      if not pre_order: print(p, end=' ')

  def dfs_demo(self, start, sort_nbrs, pre_order): # start: hex/cell, go/point
    print('\ndfs from ', start, 'with nbrs', 
          '' if sort_nbrs else 'not', 'sorted',
          'pre-order' if pre_order else 'post-order')
    seen = [False]*len(self.p_range)
    self.dfs(start, seen, sort_nbrs, pre_order)
    print('')

  def bfs_demo(self, start, sort_nbrs): # start is cell in hex, point in go
    def add_to_q(p, seen, q):
      print(p, end=' ')
      seen[p] = True
      q.append(p)
      
    print('\nbfs from ', start, 'with nbrs', 
          '' if sort_nbrs else 'not', 'sorted')
    seen = [False]*len(self.p_range)
    myqueue = []
    add_to_q(start, seen, myqueue)
    while len(myqueue) > 0:
      cell = myqueue.pop(0)
      for nbr in sorted(self.nbrs[cell]) if sort_nbrs else self.nbrs[cell]:
        if not seen[nbr]: add_to_q(nbr, seen, myqueue)
    print('')

  def __init__(self): 
    self.p_range = range(3)
    self.stones = [set(), set()]  # start with empty board

    ### dictionaries
    self.nbrs      = {} # point -> neighbors
    self.blocks    = {} # point -> block
    self.liberties = {} # point -> liberties
    self.parents   = {} # point -> parents in block

    for point in self.p_range:
      self.nbrs[point]      = set()
      self.blocks[point]    = set()
      self.liberties[point] = set()
      self.parents[point]    = point

    for j in self.p_range:
      for k in self.p_range:
         if j != k: self.nbrs[j].add(k)

    IO.show_dict('point neighbor sets', self.nbrs)

    self.add_stone(Cell.b, 0)
    for p in self.p_range:
      self.liberties[p].update(self.nbrs[p])
    self.show_parents()
    self.show_liberties()

    self.add_stone(Cell.b, 2)
    for p in self.p_range:
      self.liberties[p].update(self.nbrs[p])
    self.show_parents()
    self.show_liberties()
