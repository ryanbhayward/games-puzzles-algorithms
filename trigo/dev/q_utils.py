"""
  game of go on a 4-point board  rbh 2024
      
      . .     cell names  3 0
      . .                 2 1
"""

from string import ascii_lowercase

class Cell: ############## board cells ###############
  b, w, e = '*', 'o', '.' # black, white, empty
  io_ch = b+w+e
  n = 4   # 4 cells on trigo board
  cells = (0,1,2,3)

  def name(c): return ('black','white','empty')[Cell.io_ch.index(c)]

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
  b, w, p, nil = Cell.b, Cell.w, 'pass', ' nil'

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
  def board_show(brd):
    s = '\n 3 0  '+ brd[3]+' '+brd[0] + '\n 2 1  '+brd[2]+' '+brd[1]+\
        '  score ' + str(Board.score(brd))
    return Color.paint(s, Cell.io_ch)

  def change_string(p, where, ch):
    return p[:where] + ch + p[where+1:]

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])

  welcome = Color.mgn('\n    trigo    ')+\
    Color.grn(' go on a 3-cell board\n')+\
    Color.mgn(' usual rules ')+\
    Color.grn(' Tromp-Taylor no-suicide\n')

  menu =  Color.mgn(' b pass')+'     black pass\n' +\
    Color.mgn(' w 2   ')+'     play white: cell 2\n' +\
    Color.mgn('  u    ')+'     undo\n' +\
    Color.mgn(' [return]')+'   quit\n'

class Board:
  def empty():
    return Cell.e * Cell.n  # all empty cells 

  def report(brd): 
    print(IO.board_show(brd))
    #print(' ? black moves', 
    #  Board.legal_moves(brd, Cell.b))
    #print(' ? white moves', 
    #  Board.legal_moves(brd, Cell.w))

  def change_cell(brd, color, where):
    assert(where in range(Cell.n))
    assert(color in (Cell.b, Cell.w, Cell.e))
    assert(color == Cell.e or brd[where] == Cell.e)
    return IO.change_string(brd, where,  color)
  
  def clear_color(brd, color):
    return ''.join([Cell.e if c == color else c for c in brd])

  def counts(brd, color):
    return brd.count(color), brd.count(Cell.opponent(color))

  def has_liberty(brd, j, color):
    c0, c1, c2 = (j+1)%4, (j+2)%4, (j+3)%4
    return (brd[c0] == Cell.e) or (brd[c2] == Cell.e) or \
      ((brd[c0] == color) and (brd[c1] == Cell.e)) or \
      ((brd[c2] == color) and (brd[c1] == Cell.e))

  def can_play(brd, j, color):
    new = IO.change_string(brd, j, color)
    c0, c2 = (j+1)%4, (j+3)%4
    if (brd[c0] == Cell.opponent(color) and
      not Board.has_liberty(new, c0, Cell.opponent(color))) or \
       (brd[c2] == Cell.opponent(color) and
      not Board.has_liberty(new, c2, Cell.opponent(color))):
      new = Board.clear_color(new, Cell.opponent(color))
    if Board.has_liberty(new, j, color):
      return True, new
    return False, ''

  def children(brd, color):
    kids = []
    for j in Cell.cells:
      if brd[j] == Cell.e:
        ok, new = Board.can_play(brd, j, color)
      if ok: kids.append((j,new))
    return kids

  def is_legal(brd):
    bcount = brd.count(Cell.b)
    wcount = brd.count(Cell.w)
    ecount = 4 - (bcount + wcount)
    if ecount == 0: return False
    if ecount >= 2: return True
    if bcount == 0 or wcount == 0: return True
    # total 3 b,w, at least 1 of each
    return (brd[0] == Cell.e and brd[3] != brd[1]) or \
           (brd[1] == Cell.e and brd[0] != brd[2]) or \
           (brd[2] == Cell.e and brd[1] != brd[3]) or \
           (brd[3] == Cell.e and brd[2] != brd[0])

  def score(brd):
    if Board.is_legal(brd):
      bcount = brd.count(Cell.b)
      wcount = brd.count(Cell.w)
      if bcount == wcount: return 0
      if wcount == 0: return 4
      if bcount == 0: return -4
      return 1 if bcount > wcount else -1
    print('      illegal position ', end='')

  def test(p):
    print('Board tests\n')
    for color in (Cell.b, Cell.w):
      for j in range(Cell.n):
        p = Board.change_cell(p, color, j)
        Board.report(p)
      for j in range(Cell.n):
        p = Board.change_cell(p, Cell.e, j)
        Board.report(p)
    p = Board.change_cell(p, Cell.b, 2)
    p = Board.change_cell(p, Cell.w, 1)
    Board.report(p)
