"""
  * simple go environment    rbh 2024
      ? class Cell: empty/B/W 0,1/2, opponent
      ? blocks and liberties
      ? legal moves
      ? tromp taylor score
      ? bring stuff over from other program
"""

from string import ascii_lowercase
from go_io import Color, IO

#################################################
class go_board:
  BLK, WHT, EMP, IO_CHRS  = 0, 1, 2, '*o.'
  COLORS = (BLK, WHT)

  ######## cell_color to character
  def point_str(self, p):
    if   p in self.stones[self.BLK]: return '*'
    if   p in self.stones[self.WHT]: return 'o'
    return '.'  # if not B/W must be EMP

  def board_str(self):
    return ''.join([self.point_str(p) for p in range(self.n)])
  ########

  #def opponent(self, player):
  #  assert player in self.COLORS, 'player not BLK/WHT'
  #  return 1 - player

  def rc_point(self, y, x):
    return x + y * self.c
  
  def point_color(self, p):
    if p in self.stones[self.BLK]: return self.BLK
    if p in self.stones[self.WHT]: return self.WHT
    return self.EMP

  def show_blocks(self):
    for pcol in self.COLORS:
      print(self.IO_CHRS[pcol], 'blocks', end=' ')
      for p in range(self.n):
        if self.point_color(p) == pcol and self.is_root(p):
          print(self.blocks[p], end=' ')
      print()
      print(self.IO_CHRS[pcol], 'liberties', end=' ')
      for p in range(self.n):
        if self.point_color(p) == pcol and self.is_root(p):
          print(self.liberties[p], end=' ')
      print()

  def print(self):
    bs, r, c = self.board_str(), self.r, self.c
    IO.show_board(bs, r, c)
  #  outs = '\n'
  #  for y in reversed(range(r)):
  #    outs += f'{y+1:2} '+ spread(bs[y*c:(y+1)*c]) + '\n'
  #  outs += '\n   ' + spread(ascii_lowercase[:c])
  #  print(Color.paint(outs))
  #  self.show_blocks()

  def show_point_names(self):  # confirm names look ok
    print('\nnames of points\n')
    for y in range(self.r - 1, -1, -1): #print last row first
      for x in range(self.c):
        print(f'{self.rc_point(y, x):3}', end='')
      print()

  def is_root(self, p):
    return self.parent[p] == p

  def merge_blocks(self, p, q):
    print('merge blocks', p, q)
    proot = UF.find(self.parent, p)
    qroot = UF.find(self.parent, q)
    # proot will be root of merged block
    self.parent[qroot] = proot
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
    point, stns = self.rc_point(r, c), self.stones

    assert color in self.COLORS, 'invalid color'
    assert point not in stns[self.BLK].union(stns[self.WHT]), \
           'already a stone there'

    stns[color].add(point)
    self.blocks[point].add(point)

    for n in self.nbrs[point]:
      if n in self.stones[color]: # same-color nbr
        self.merge_blocks(n, point)
      if n in self.stones[1 - color]: # opponent nbr
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
    self.show_point_names()

    for y in range(self.r):
      for x in range(self.c):
        p = self.rc_point(y,x)
        if x > 0: 
          self.nbrs[p].add( self.rc_point(y, x - 1) )
        if x < self.c - 1: 
          self.nbrs[p].add( self.rc_point(y, x + 1) )
        if y > 0: 
          self.nbrs[p].add( self.rc_point(y - 1, x) )
        if y < self.r - 1: 
          self.nbrs[p].add( self.rc_point(y + 1, x) )

    for p in range(self.n):
      self.liberties[p].update(self.nbrs[p])

    print('\nliberties\n')
    for p in range(self.n):
      print(f'{p:2}', self.liberties[p])
    #print('\nneighbors of points\n')
    #for p in self.nbrs: print(f'{p:2}', self.nbrs[p])
    #self.show_point_names()

################################ not using this yet
class UF:        # union find

  def union(parent,x,y):
    parent[x] = y
    return y

  def find(parent, x):
    while x != parent[x]:
      x = parent[x]
    return x

 # if you perform millions of UF opertions, this is better:
 # def find(parent,x): # with grandparent compression
 #   while True:
 #     px = parent[x]
 #     if x == px: return x
 #     gx = parent[px]
 #     if px == gx: return px
 #     parent[x], x = gx, gx
##################################################### 

################################ not using this yet
class go_env:
  def __init__(self, r, c):
    self.board = go_board(r,c)
##################################################### 

m45demo = ((0,1,0),(1,1,2),(1,1,4),(1,0,3),(1,2,3), \
           (0,3,0),(1,1,3),(0,2,1),(0,2,0),(0,3,3))

m22demo = ((0,0,0),(1,0,1),(0,1,1),(1,1,0))

#gb = go_board(4,5)
#for move in m45demo:
gb = go_board(2,2)
for move in m22demo:
  gb.add_stone(move[0], move[1], move[2])
  gb.print()
