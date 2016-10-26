# hex player              RBH 2016
# style influenced by 
#   * Michi (by Petr Baudis)
#   * Morat (by Timo Ewalds)
#   * Miaowy (by RBH)
#   * Benzene (by 
#       Broderick Arneson, Philip Henderson, Jakub Pawlewicz,
#       Aja Huang, Yngvi Bjornsson, Michael Johanson, Morgan Kan,
#       Kenny Young, Noah Weninger, RBH)

import numpy as np

class Cell: #############  cells #########################
  e,b,w,ch = 0,1,2, '.*@-'       # empty, black, white

  def opponent(c): 
    return 3-c

class B: ################ the board #######################

  ### i-o variables
  letters = 'abcdefghijklmnopqrstuvwxyz'
  esc       = '\033['            ###### these are for colors
  endcolor  =  esc + '0m'
  textcolor =  esc + '0;37m'
  color_of  = (textcolor, esc + '0;35m', esc + '0;32m')

  def __init__(self,rows,cols):
    self.r  = rows  
    self.c  = cols
    self.n  = rows*cols   # number cells
    self.g  = 1   # number guard layers that encircle true board
    self.w  = self.c + self.g + self.g  # width of layered board
    self.fat_n = self.w * (self.r + self.g + self.g) # fat-board cells

# 2x3 board  layers: g==1    g==2      
#                           *******
#            *****           *******
#    ...      o...o           oo...oo
#     ...      o...o           oo...oo
#               *****           *******
#                                *******
    
    self.empty_brd = np.array([0]*self.n, dtype=np.int8)
    self.empty_fat_brd = np.array(
      ([Cell.b]*self.w) * self.g +
      ([Cell.w]*self.g + [0]*self.c + [Cell.w]*self.g) * self.r +
      ([Cell.b]*self.w) * self.g, dtype=np.int8)

# 2x3 board      r,c          positions

#    ...      0 0  0 1  0 2     0  1  2
#     ...      1 0  1 1  1 2     3  4  5

# 2x3 fat board     r,c                 positions

#  -***-     -1-1 -1 0 -1 1 -1 2 -1 3    0  1  2  3  4
#   o...o     0-1   0 0  0 1  0 2  0 3    5  6  7  8  9
#    o...o     1-1   1 0  1 1  1 2  1 3   10 11 12 13 14
#     -***-     2-1   2 0  2 1  2 2  2 3   15 16 17 18 19

### board i-o ##############
  def disp(self, brd): # for true boards, add outer layers
    assert(len(brd)==self.n)
    s = 2*' ' + ' '.join(self.letters[0:self.c]) + '\n'
    for j in range(self.r):
      s += j*' ' + '{:2d}'.format(j) + ' ' + \
        ' '.join([Cell.ch[brd[k + j*self.c]] for k in \
        range(self.c)]) + ' ' + Cell.ch[Cell.w] + '\n'
    return s + (3+self.r)*' ' + ' '.join(Cell.ch[Cell.b]*self.c) + '\n'

  def disp_fat(self, brd): # for fat boards, just print board
    assert(len(brd)==self.fat_n)
    s = ''
    for j in range(self.r + self.g + self.g):
      s += j*' ' + ' '.join([Cell.ch[brd[k + j*self.w]] \
        for k in range(self.w)]) + '\n'
    return s
     
#    powers_of_3 = [1]
    #for j in range(self.n-1): 
      #powers_of_3.append(powers_of_3[j])
    #self.powers_of_3 = np.array(powers_of_3)

#  def brd_to_int(self,brd):
#    return sum(brd*self.powers_of_3) # numpy multiplies vectors componentwise

  def psn_of(self,x,y):
    return x*self.c + y

  def fat_psn_of(self,x,y):
    return (x+ self.g)*self.w + y + self.g

  def rc_of(self, p): # return usual row, col coordinates
    return divmod(p, self.c)

  def rc_of_fat(self, p):  # return usual row, col coordinates
    x,y = divmod(p, self.w)
    return x - self.g, y - self.g

  def paint(self,s):  # s   a string
    p = ''
    for c in s:
      x = Cell.ch.find(c)
      if x >= 0:
        p += self.color_of[x] + c + self.endcolor
      elif c.isalnum():
        p += self.textcolor + c + self.endcolor
      else: p += c
    return p

### user i-o

def tst(r,c):
  b = B(r,c)
  print(b.disp(b.empty_brd))
  print(b.paint(b.disp(b.empty_brd)))
  print(b.disp_fat(b.empty_fat_brd))
  print(b.paint(b.disp_fat(b.empty_fat_brd)))

  for r in range(b.r):
    for c in range(b.c):
      p = b.psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == (b.rc_of(p))
    print('')

  p = 0
  for r in range(-b.g, b.r + b.g):
    for c in range(-b.g, b.c + b.g):
      p = b.fat_psn_of(r,c)
      #print(r,c,p,b.rc_of_fat(p))
      print('{:3}'.format(p), end='')
      assert (r,c) == (b.rc_of_fat(p))
    print('')

## consider all possible isomorphic positions, return min
#def min_iso(L): # using numpy array indexing here
  #return min([brd_to_int( L[Isos[j]] ) for j in range(8)])

# convert from integer for board position
#def base_3( y ): 
#  assert(y <= ttt_states)
#  L = [0]*Cell.n
#  for j in range(Cell.n):
#    y, L[j] = divmod(y,3)
#    if y==0: break
#  return np.array( L, dtype = np.int16)

# input-output ################################################
def char_to_cell(c): 
  return Cell.chars.index(c)

def genmoverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid genmove request\n')
  if len(cmd)==2:
    x = Cell.chars.find(cmd[1][0])
    if x == 1 or x == 2:
      return True, cmd[1][0], ''
  return invalid

def printmenu():
  print('  x b2         play x b 2')
  print('  o e3         play o e 3')
  print('  . a2          erase a 2')
  print('  u                  undo')
  print('  ?           solve state')
  print('  g x/o           genmove')
  print('  t      use trans. table')
  print('  [return]           quit')

  #def putstone(self, row, col, color):
  #  self.brd[rc_to_lcn(row,col)] = color

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    lcn = H.pop()
    brd[lcn] = Cell.e

tst(2,3)
tst(3,2)
tst(6,6)
tst(11,11)
