"""
  go on a triangle (based on hexgo)      rbh 2024
      
       .     cell names   0
      . .                1 2
"""

from string import ascii_lowercase

class Cell: ############## board cells ###############
  b, w, e, io_ch = 0, 1, 2, '*@.'  # black, white, empty

  def from_ch(ch): return Cell.io_ch.index(ch)

  def opponent(c): return 1 - c

  def test():
    print('tests for class Cell')
    io_ch = Cell.io_ch
    for ch in io_ch:
      c = Cell.from_ch(ch)
      print(ch, c, io_ch[c])
    print()
    for j in range(2):
      print(j, Cell.opponent(j))

class Color: ############ for color output ############
  green   = '\033[0;32m'
  magenta = '\033[0;35m'
  grey    = '\033[0;37m'
  end     = '\033[0m'

  def paint(s, chrs):
    p = ''
    for c in s:
      if c == chrs[0]: p += Color.magenta + c + Color.end
      elif c == chrs[1]: p += Color.green + c + Color.end
      elif c.isalpha(): p+= Color.magenta + c + Color.end
      elif c.isnumeric(): p+= Color.green + c + Color.end
      elif c.isprintable(): p += Color.grey + c + Color.end
      else: p += c
    return p

class IO:  ############## hex and go output #############

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])
  
  def point_ch(stone_sets, p):
    if p in stone_sets[0]: return Cell.io_ch[0]
    if p in stone_sets[1]: return Cell.io_ch[1]
    return Cell.io_ch[2]

  def board_str(stone_sets, n):
    return ''.join([IO.point_ch(stone_sets, p) for p in range(n)])

  def show_pairs(msg, d):
    print('\n' + msg)
    for x in d: print(x, d[x], end=' : ')
    print()

  def show_dict(msg, d):
    print('\n' + msg)
    for x in d: print(x, d[x])

  def disp(state): 
    s = '  ' + state.board[0] + '\n' + IO.spread(state.board[1:])
    print(Color.paint(s, Cell.io_ch))
    print('      score ', state.score(), 'empty cells', state.empty_cells())

  def test():
    print('tests for class IO\n')
    for color in (Cell.b, Cell.w):
      state = Board()
      IO.disp(state)
      for j in range(state.n):
        state.color_cell(color, j)
        IO.disp(state)
    for j in range(state.n):
      state.color_cell(Cell.e, j)
      IO.disp(state)
    state.color_cell(Cell.b, 2)
    IO.disp(state)
    state.color_cell(Cell.w, 1)
    IO.disp(state)

class Pt: ############## board points     ###############

  def point_color(stones, p):
    if p in stones[Cell.b]: return Cell.b
    if p in stones[Cell.w]: return Cell.w
    return Cell.e

class Board:
  n = 3        # only 3 cells :)

  def __init__(self):
    self.board = Cell.io_ch[Cell.e] * self.n
    self.history = [self.board]
    print('init board', self.board)
    print('init history', self.history)
  
  def color_cell(self, color, where):
    assert(where in (0,1,2))
    assert(color in (Cell.b, Cell.w, Cell.e))
    assert(color == Cell.e or self.board[where] == Cell.io_ch[Cell.e])
    self.board = self.board[:where] + Cell.io_ch[color] + self.board[where+1:]

  def is_legal(self):
    return Cell.io_ch[Cell.e] in self.board

  def empty_cells(self):
    empties = [j for j, x in enumerate(self.board) if x == Cell.io_ch[Cell.e]]
    return empties

  def legal_moves(self, color):
    assert(color in (Cell.b, Cell.w))
    assert self.is_legal()
    bcount = self.board.count(Cell.io_ch[Cell.b])
    wcount = self.board.count(Cell.io_ch[Cell.w])
    return self.empty_cells()

  def score(self):
    if self.is_legal():
      bcount = self.board.count(Cell.io_ch[Cell.b])
      wcount = self.board.count(Cell.io_ch[Cell.w])
      if bcount == 2 or bcount > wcount: return 1
      if wcount == 2 or bcount < wcount: return -1
      return 0
    else:
      print('      illegal position ', end='')
