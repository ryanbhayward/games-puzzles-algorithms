"""
  * simple go environment    rbh 2024
      - blocks and liberties
      ? legal moves
      ? tromp taylor score
      ? interact
"""

from hexgo import Cell, Color, IO, Pt, UF

#################################################
class go_board:

  def print(self):
    IO.disp_go(IO.board_str(self.stones, self.n), self.r, self.c)

  def show_point_names(self):  # confirm names look ok
    print('\nnames of points\n')
    for y in range(self.r - 1, -1, -1): #print last row first
      for x in range(self.c):
        print(f'{Pt.rc_point(y, x, self.c):3}', end='')
      print()

  def merge_blocks(self, p, q):
    print('merge blocks', p, q)
    proot, qroot = UF.union(self.parent, p, q)
    self.blocks[proot].update(self.blocks[qroot])
    self.liberties[proot].update(self.liberties[qroot])
    self.liberties[proot] -= self.blocks[proot]

  def remove_liberties(self, p, q): 
    proot = UF.find(self.parent, p)
    qroot = UF.find(self.parent, q)
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

  def __init__(self, r, c): 

    ### r horizontal lines, c vertical lines, r*c points

    self.r, self.c, self.n = r, c, r * c

    self.stones = [set(), set()]  # start with empty board

    ### dictionairies
    self.nbrs      = {} # point -> neighbors
    self.blocks    = {} # point -> block
    self.liberties = {} # point -> liberties
    self.parent    = {} # point -> parent in block

    for point in range(self.n):
       self.nbrs[point]      = set()
       self.blocks[point]    = set()
       self.liberties[point] = set()
       self.parent[point]    = point

    print('\nparent of points\n')
    for p in range(self.n): 
      print(f'{p:2}', self.parent[p])
    Pt.show_go_point_names(self.r, self.c)

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
class go_env:
  def __init__(self, r, c):
    self.board = go_board(r,c)
##################################################### 

m22demo = ((0,0,0),(1,0,1),(0,1,1),(1,1,0))
m45demo = ((0,1,0),(1,1,2),(1,1,4),(1,0,3),(1,2,3), \
           (0,3,0),(1,1,3),(0,2,1),(1,2,0),(0,3,3))

gb = go_board(4,5)
for move in m45demo:
#gb = go_board(2,2)
#for move in m22demo:
  gb.add_stone(move[0], move[1], move[2])
  gb.print()
IO.show_blocks(gb.n, gb.stones, gb.parent, gb.blocks, gb.liberties)
