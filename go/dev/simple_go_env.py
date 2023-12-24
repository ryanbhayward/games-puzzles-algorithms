"""
  * simple go environment    rbh 2024
      ? legal moves
      ? tromp taylor score
  todo 
    - start to bring stuff over from other program
"""

from string import ascii_lowercase

### IO ##############################################
def embed_blanks(s): # embed blanks in string
  return ''.join([' ' + c for c in s])

class go_board:
  BLACK, WHITE, EMPTY  = 0, 1, 2
  COLORS = (BLACK, WHITE)

  ######## color to character
  def point_str(self, p):
    if   p in self.stones[self.BLACK]: return '*'
    if   p in self.stones[self.WHITE]: return 'o'
    return '.'  # if not B/W must be EMPTY

  def board_str(self):
    return ''.join([self.point_str(p) for p in range(self.n)])
  ########

  #def opponent(self, player):
  #  assert player in self.COLORS, 'player not BLACK/WHITE'
  #  return 1 - player

  def rc_point(self, y, x):
    return x + y * self.cols

  def show_board(self):
    bstr = self.board_str()
    print('')
    for y in range(self.rows - 1, -1, -1): #print last row first
      print(f'{y+1:2} ' + embed_blanks(bstr[y*self.cols : (y + 1)*self.cols]))
    print('\n   ' + embed_blanks(ascii_lowercase[0:self.cols]))

  def show_point_names(self):  # confirm names look ok
    print('\nnames of points\n')
    for y in range(self.rows - 1, -1, -1): #print last row first
      for x in range(self.cols):
        print(f'{self.rc_point(y, x):3}', end='')
      print()

  def add_stone(self, color, r, c):
    assert color in self.COLORS, 'invalid color'
    stns, point = self.stones, self.rc_point(r, c)
    assert point not in stns[self.BLACK].union(stns[self.WHITE]), 'already a stone there'
    stns[color].add(point)

  def __init__(self, r, c): 

    ### r horizontal lines, c vertical lines, r*c points

    self.rows, self.cols, self.n = r, c, r * c

    ### neighbors of each point

    self.nbrs = {} # dictionary:  point -> neighbors
    
    for point in range(self.n):
       self.nbrs[point] = set()

    for y in range(self.rows):
      for x in range(self.cols):
        p = self.rc_point(y,x)
        if x > 0: 
          self.nbrs[p].add( self.rc_point(y, x - 1) )
        if x < self.cols - 1: 
          self.nbrs[p].add( self.rc_point(y, x + 1) )
        if y > 0: 
          self.nbrs[p].add( self.rc_point(y - 1, x) )
        if y < self.rows - 1: 
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
gb.add_stone(gb.BLACK, 1, 0)
gb.show_board()
gb.add_stone(gb.WHITE, 1, 2)
gb.show_board()
gb.add_stone(gb.WHITE, 1, 3)
gb.show_board()
gb.add_stone(gb.BLACK, 2, 4)
gb.show_board()
