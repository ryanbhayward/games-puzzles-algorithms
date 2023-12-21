"""
  * go_simple.py    rbh 2024
      ? legal moves
      ? tromp taylor score
  * allow rectangular boards
             1 <= R <= 19 rows 
             1 <= C <= 19 columns
  todo * check whether position is legal
       * put more inside Game_state ?
"""

from string import ascii_lowercase

class go_board:
  BLACK, WHITE, EMPTY = 0, 1, 2

  def opponent(self, clr):
    assert(clr == self.BLACK or clr == self.WHITE)
    return 1 - clr

  def __init__(self, r, c):

    ### go board: r horizontal lines, c vertical lines, r*c points

    self.rows, self.cols, self.n = r, c, r * c

    def rc_point(y, x):
      return x + y * self.cols

    def show_points(self):
      print('\nnames of points of the go board\n')
      for y in range(self.rows - 1, -1, -1): #print last row first
        for x in range(self.cols):
          print(f'{rc_point(y, x):3}', end='')
        print()

    ### neighbors of each point

    self.nbrs = {} # dictionary:  point -> neighbors
    
    for point in range(self.n):
       self.nbrs[point] = set()

    for y in range(self.rows):
      for x in range(self.cols):
        p = rc_point(y,x)
        if x > 0: 
          self.nbrs[p].add( rc_point(y, x - 1) )
        if x < self.cols - 1: 
          self.nbrs[p].add( rc_point(y, x + 1) )
        if y > 0: 
          self.nbrs[p].add( rc_point(y - 1, x) )
        if y < self.rows - 1: 
          self.nbrs[p].add( rc_point(y + 1, x) )
    
    def show_nbrs(self):    
      print('\nneighbors of points of the go board\n')
      for p in self.nbrs:
        print(f'{p:2}', self.nbrs[p])

    ### stones
    self.stones = [set(), set()]

    def point_str(self, p):
      if   p in self.stones[self.BLACK]: return '*'
      elif p in self.stones[self.WHITE]: return 'o'
      else:                    return '.'

    def show_stones(self):
      print('\nstones of the go board\n')
      print('  ', end='')
      for x in range(self.cols):
        print(' ' + ascii_lowercase[x], end='')
      print()
      for y in range(self.rows - 1, -1, -1): #print last row first
        thisrow = f'{y+1:2}'
        for x in range(self.cols):
          thisrow += ' ' + point_str(self, rc_point(y, x))
        print(thisrow)

    show_points(self)
    show_nbrs(self)
    self.stones[self.BLACK].add(rc_point(1, 1))
    self.stones[self.WHITE].add(rc_point(0, 0))
    show_stones(self)
    print()

go_board(4,6)
