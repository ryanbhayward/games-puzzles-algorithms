"""
  * simple go environment    rbh 2024
      ? legal moves
      ? tromp taylor score
  todo 
    - start to bring stuff over from other program
"""

from string import ascii_lowercase

### IO ##############################################
def spread(s): # embed blanks in string
  return ''.join([' ' + c for c in s])

class go_board:
  BLK, WHT, EMP  = 0, 1, 2
  COLORS = (BLK, WHT)

  ######## color to character
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

  def show_board(self):
    bs, r, c = self.board_str(), self.r, self.c
    print('')
    for y in reversed(range(r)):
      print(f'{y+1:2} '+ spread(bs[y*c:(y+1)*c]))
    print('\n   ' + spread(ascii_lowercase[:c]))

  def show_point_names(self):  # confirm names look ok
    print('\nnames of points\n')
    for y in range(self.r - 1, -1, -1): #print last row first
      for x in range(self.c):
        print(f'{self.rc_point(y, x):3}', end='')
      print()

  def add_stone(self, color, r, c):
    assert color in self.COLORS, 'invalid color'
    stns, point = self.stones, self.rc_point(r, c)
    assert point not in stns[self.BLK].union(stns[self.WHT]), 'already a stone there'
    stns[color].add(point)

  def __init__(self, r, c): 

    ### r horizontal lines, c vertical lines, r*c points

    self.r, self.c, self.n = r, c, r * c

    ### neighbors of each point

    self.nbrs = {} # dictionary:  point -> neighbors
    
    for point in range(self.n):
       self.nbrs[point] = set()

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

    self.stones = [set(), set()]  # empty board to start

    #print('\nneighbors of points\n')
    #for p in self.nbrs: print(f'{p:2}', self.nbrs[p])
    #self.show_point_names()

################################ not using this yet
class UF:        # union find

  def union(parent,x,y):
    parent[x] = y
    return y

  def find(parent,x): # with grandparent compression
    while True:
      px = parent[x]
      if x == px: return x
      gx = parent[px]
      if px == gx: return px
      parent[x], x = gx, gx
##################################################### 

################################ not using this yet
class go_env:
  def __init__(self, r, c):
    self.board = go_board(r,c)
##################################################### 

gb = go_board(4,5)
gb.add_stone(gb.BLK, 1, 0)
gb.show_board()
gb.add_stone(gb.WHT, 1, 2)
gb.show_board()
gb.add_stone(gb.WHT, 1, 3)
gb.show_board()
gb.add_stone(gb.BLK, 2, 4)
gb.show_board()
