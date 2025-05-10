"""
  rbh 2025
  for hex.py, based on hexgo.py   
  classes Cell, Color, Game, IO, Pt, UF
  
  TODO: just started
"""

from string import ascii_lowercase

class Cell: ############## board cells ###############
  b, w, e, io_ch = 0, 1, 2, '*@.'  # black, white, empty
  bw = (b, w)

  def from_ch(ch): return Cell.io_ch.index(ch)

  def opponent(c): return 1 - c

  def test():
    print('tests for class Cell')
    io_ch = Cell.io_ch
    for ch in io_ch:
      c = Cell.from_ch(ch)
      outstr = ch + ' ' + str(c) + ' ' + io_ch[c]
      print(Color.paint(outstr, Cell.io_ch))
    print()
    print('opponent test')
    for j in range(2):
      print(j, Cell.opponent(j))

class Board: ############ string  ############
  def color_cell(psn, where, color):
    return psn[:where] + color + psn[where+1:]

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

class IO:  ############## hex output #############

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])
  
  def point_ch(brd, p):
    return brd[p]

  def show_dict(msg, d):
    print('\n' + msg)
    for x in d: print(x, d[x])

  def disp(brd, r, c): 
    s = '\n'
    s += '  ' + IO.spread(ascii_lowercase[:c]) + '\n'
    for y in range(r):
      s += y*' ' + f'{y+1:2} ' +IO.spread(brd[y*c:(y+1)*c])
      s += ' ' + Cell.io_ch[Cell.w] + '\n'
    s += '   ' + ' '*r + (' ' + Cell.io_ch[Cell.b])*c
    print(Color.paint(s, Cell.io_ch))

class Pt: ############## board points     ###############

  def rc_point(row, col, num_cols):
    return col + row * num_cols

  def rc_of(self, p): # return usual row, col coordinates
    return divmod(p, B.c)

Cell.test()
