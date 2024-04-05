"""
  go on a triangle (based on hexgo)      rbh 2024
      
       .     cell names   0
      . .                1 2
"""

from string import ascii_lowercase

class Cell: ############## board cells ###############
  b, w, e = '*', '@', '.' # black, white, empty
  io_ch = b+w+e

  def opponent(c): 
    if c == Cell.e: return None
    return Cell.b if c == Cell.w else Cell.w

  def test():
    print('\n  Cell test   ', end='')
    for ch in Cell.io_ch: 
      print(ch, '', end='')
    print('\n   opponents  ', end='')
    for j in Cell.io_ch: 
      print(j, Cell.opponent(j), end='  ')
    print()

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

class IO:  ############## input/output, strings #############

  def change_string(p, where, ch):
    return p[:where] + ch + p[where+1:]

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])
  
  def board_str(board):
    s = '  ' + board[0] + '\n' + IO.spread(board[1:])
    return Color.paint(s, Cell.io_ch)

  #def show_pairs(msg, d):
  #  print('\n' + msg)
  #  for x in d: print(x, d[x], end=' : ')
  #  print()

  #def show_dict(msg, d):
  #  print('\n' + msg)
  #  for x in d: print(x, d[x])

  def disp(state): 
    print(IO.board_str(state.board))
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

class Board:
  n = 3        # trigo board: only 3 cells   :)

  def __init__(self):
    self.board = Cell.e * self.n
    self.history = [self.board]
    print('init board', self.board)
    print('init history', self.history)
  
  def color_cell(self, color, where):
    assert(where in (0,1,2))
    assert(color in (Cell.b, Cell.w, Cell.e))
    assert(color == Cell.e or self.board[where] == Cell.e)
    self.board = IO.change_string(self.board, where,  color)

  def is_legal(self):
    return Cell.e in self.board

  def empty_cells(self):
    empties = [j for j, x in enumerate(self.board) if x == Cell.e]
    return empties

  def legal_moves(self, color):
    assert(color in (Cell.b, Cell.w))
    assert self.is_legal()
    bcount = self.board.count(Cell.b)
    wcount = self.board.count(Cell.w)
    return self.empty_cells()

  def score(self):
    if self.is_legal():
      bcount = self.board.count(Cell.b)
      wcount = self.board.count(Cell.w)
      if bcount == 2 or bcount > wcount: return 3
      if wcount == 2 or bcount < wcount: return -3
      return 0
    else:
      print('      illegal position ', end='')
