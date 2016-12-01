# simple program to play linear go
import sys
from paint_chars import paint
# add move history

class Linear_go_state:
  def __init__(self,numcells):
    self.Black, self.White, self.Empty, self.Edge = range(4)
    self.stone = '*o-%'  # black white empty edge
    self.n = numcells

    # board as string
    self.b =  self.stone[self.Edge]\
            + self.stone[self.Empty] * numcells\
            + self.stone[self.Edge]

    # for locations of cells that are left-end or right-end of a group,
    #   the number of cells in that group
    self.size = [1] * (numcells+2)
    self.h = [ self.b ]  # history

  def erase_stones(self,psn,k):
    self.b = self.b[:psn] + self.stone[self.Empty]*k + self.b[psn+k:]
    for j in range(psn,psn+k): self.size[j] =1

  def add_cell(self,psn,color):
    self.b = self.b[:psn] + self.stone[color] + self.b[psn+1:]
    # if new stone now in group of size > 1, update size of group
    if self.b[psn] == self.b[psn-1]:  # matches stone to its left
      if self.b[psn] == self.b[psn+1]:  # matches stone to its right
        newsize = 1 + self.size[psn-1] + self.size[psn+1]
        self.size[psn-self.size[psn-1]] = newsize  #update on left end
        self.size[psn+self.size[psn+1]] = newsize  #update on right end
      else:  # matches on left but not right
        newsize = 1 + self.size[psn-1]
        self.size[psn-self.size[psn-1]] = newsize  #update on left end
        self.size[psn] = newsize                   #update on right end
    elif self.b[psn] == self.b[psn+1]:  # matches right but not left
      newsize = 1 + self.size[psn+1]
      self.size[psn] = newsize                    #update on left end
      self.size[psn+self.size[psn+1]] = newsize   #update on right end

  def is_empty(self,psn):
    return self.b[psn] == self.stone[self.Empty]

  #def leftGroupStrong(self,psn): # group to left has 2nd liberty ?
    #assert(self.is_empty(psn) and not self.is_empty(psn-1))
    #return self.is_empty(psn-self.size[psn-1])
#
  #def rightGroupStrong(self,psn): # group to right has 2nd liberty ?
    #assert(self.is_empty(psn) and not self.is_empty(psn+1))
    #return self.is_empty(psn+self.size[psn+1])

  def left_capture(self, psn, color):  # move will capture left group ?
    return (self.b[psn-1] == self.stone[1-color] and
       not self.is_empty(psn-(1+self.size[psn-1])))

  def right_capture(self, psn, color):  # move will capture right group ?
    return (self.b[psn+1] == self.stone[1-color] and
       not self.is_empty(psn+(1+self.size[psn+1])))
  
  def is_legal_move(self, psn, color):
    return self.is_empty(psn) and (
      self.is_empty(psn-1) or self.is_empty(psn+1) or
      (self.b[psn-1] == self.stone[color] and
       self.is_empty(psn-(1+self.size[psn-1]))) or
      (self.b[psn+1] == self.stone[color] and
       self.is_empty(psn+1+self.size[psn+1])) or
       self.left_capture(psn,color) or
       self.right_capture(psn,color) )

  def make_legal_move(self, psn, color):
    assert self.is_legal_move(psn,color)
    if self.left_capture(psn,color):
      self.erase_stones(psn-self.size[psn-1],self.size[psn-1])
    if self.right_capture(psn,color):
      self.erase_stones(psn+1, self.size[psn+1])
    self.add_cell(psn, color)
    self.h.append(self.b)

  def show_history(self):
    for j in range(len(self.h)):
      print('  ', '{0:3d}'.format(j), self.h[j][1:-1])
    print('')

  def show(self):
    self.show_history()
    sizestr = ''   # print group sizes
    for j in range(2 + self.n):
      if self.size[j] < 10:
        sizestr += ' '
      sizestr += ' ' + str(self.size[j])

    indexstr = '   '  # print cell indices
    for j in range(self.n):
      if j + 1 < 10:
        indexstr += ' '
      indexstr += ' ' + str(j+1)

    cellstr = ''    # then print cell contents
    for c in self.b:
      cellstr += '  ' + c
    print(paint(indexstr + '\n' + cellstr + '\n' + sizestr, self.stone))

    for ptm in range(2):
      print('\n  legal ' + self.stone[ptm] + ' ', end='')
      for j in range(2+self.n):
        if self.is_legal_move(j, ptm):
          print(j, end='')
    print('')
    print('  score [*, o]  ', self.score())

  def score(self):  # black territory - white territory
    territory = [0, 0]
    j, last_non_empty = 1, 0  # psn on board, psn of left edge
    while j < 1 + self.n:
      color = self.stone.index(self.b[j])
      if color < 2:  # black or white
        if last_non_empty < j-1 and (
             last_non_empty == 0 or  # left edge
             color == last_color):
          territory[color] += j - last_non_empty
        else:
          territory[color] += 1
        last_non_empty, last_color = j, color
      j += 1
    if last_non_empty > 0 and last_non_empty < j-1:
      color = self.stone.index(self.b[last_non_empty])
      territory[color] += (j-1) - last_non_empty
    return territory


def get_command(color):
  print('\n ' + color + '  cell ', end='')
  line = sys.stdin.readline()
  print('')
  if line[0] == '\n':
    return -3  # end game
  elif line.split()[0] == 'u':
    return -2  # undo
  elif not line.split()[0].isdigit():
    return -1  # bad input, retry
  else:
    return int(line.split()[0])


def playGame(state):
  ptm = state.Black  # player to move: 1st player
  while True:
    state.show()
    m = get_command(state.stone[ptm])
    if m == -3:
      break
    elif m == -2:
      print('undo\n')
      if len(state.h) > 1:
        state.h.pop()
    elif m == -1:
      print('sorry ? ... ')
    elif m == 0:
      print('  pass\n')
      state.h.append(' ')
      ptm = 1 - ptm
    elif m > state.n:
      print('out of bounds')
    elif not state.is_legal_move(m, ptm):
      print(' illegal ... try again\n')
    else:
      state.make_legal_move(m, ptm)
      ptm = 1 - ptm
  print('  adios ... sayonara ... annyeong ... zaijian ...\n')

brd = Linear_go_state(8)
playGame(brd)
