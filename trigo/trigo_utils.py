"""
  game of go on a triangular 3-point board  rbh 2024
      
       .     cell names   0
      . .                1 2
"""

from string import ascii_lowercase

class Cell: ############## board cells ###############
  b, w, e = '*', 'o', '.' # black, white, empty
  io_ch = b+w+e
  n = 3   # 3 cells on trigo board

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

class Move: ####
  b, w, p = Cell.b, Cell.w, '-'

class Color: ############ for color output ############
  green   = '\033[0;32m'
  magenta = '\033[0;35m'
  grey    = '\033[0;37m'
  end     = '\033[0m'

  def grn(s): return Color.green + s + Color.end
  def mgn(s): return Color.magenta + s + Color.end

  def paint(s, chrs):
    p = ''
    for c in s:
      if   c == chrs[0]: p += Color.mgn(c)
      elif c == chrs[1]: p += Color.grn(c)
      elif c.isalpha(): p+= Color.grn(c)
      elif c.isnumeric(): p+= Color.mgn(c)
      #elif c.isprintable(): p += Color.grey + c + Color.end
      else: p += c
    return p
   

class IO:  ############## input/output, strings #############
  def board_show(string):
    s = ' '*15 + string[0] + '\n' + ' '*13 + IO.spread(string[1:])
    return Color.paint(s, Cell.io_ch)

  def change_string(p, where, ch):
    return p[:where] + ch + p[where+1:]

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])

  welcome = Color.grn('\n welcome  :) ')+\
    Color.mgn('  go on a 3-cell board\n')+\
    Color.mgn(' logical rules ')+\
    Color.grn('(Tromp-Taylor no-suicide)\n')

  menu = Color.mgn(' cells')+Color.grn('  0')+ Color.mgn('      menu options')+\
    Color.grn('\n       1 2')+\
    Color.mgn('   b pass')+'  play black pass' +\
    Color.mgn('\n             w 2')+'     play white cell 2' +\
    Color.mgn('\n             . 0')+'     erase stone at cell 0 (not legal move)' +\
    Color.mgn('\n              u')+'          undo' +\
    Color.mgn('\n          [return]')+'       quit\n'

class Board:
  board = Cell.e * Cell.n  # trigo board: only 3 cells   :)
  
  def report(self): 
    print(IO.board_show(self.board))
    print('\n      score', self.score(), end=' ')
    print('empties', self.empty_cells())
    print('      ? black moves', self.legal_moves(Cell.b))
    print('      ? white moves', self.legal_moves(Cell.w))
    print()

  def change_cell(self, color, where):
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
    bcount = self.board.count(Cell.b)
    wcount = self.board.count(Cell.w)
    stones = bcount + wcount
    if stones != 2 or bcount == 1 or \
       (bcount == 0 and color == Cell.b) or \
       (wcount == 0 and color == Cell.w):
      return self.empty_cells()
    return []

  def score(self):
    if self.is_legal():
      bcount = self.board.count(Cell.b)
      wcount = self.board.count(Cell.w)
      if bcount == 2 or bcount > wcount: return 3
      if wcount == 2 or bcount < wcount: return -3
      return 0
    else:
      print('      illegal position ', end='')

  def test(self):
    p = self
    print('Board tests\n')
    for color in (Cell.b, Cell.w):
      for j in range(Cell.n):
        p.change_cell(color, j)
        p.report()
      for j in range(Cell.n):
        p.change_cell(Cell.e, j)
        p.report()
    p.change_cell(Cell.b, 2)
    p.change_cell(Cell.w, 1)
    p.report()
