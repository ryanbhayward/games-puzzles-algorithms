"""
  simple go io    rbh 2024
"""

from string import ascii_lowercase

class Color:
  green   = '\033[0;32m'
  magenta = '\033[0;35m'
  grey    = '\033[0;37m'
  end     = '\033[0m'

  def paint(s):
    p = ''
    for c in s:
      if c == '*':
        p += Color.green + c + Color.end
      elif c == 'o':
        p += Color.magenta + c + Color.end
      elif c.isprintable():
        p += Color.grey + c + Color.end
      else:
        p += c
    return p
### end class Color ###

class IO:
  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])
  
  def show_board(brd, r, c):
    assert (len(brd) == r*c), 'board, rows, columns inconsistent'
    outs = '\n'
    #for y in reversed(range(r)): # if you want last row first
    for y in range(r): # print row by row
      outs += f'{y+1:2} '+ IO.spread(brd[y*c:(y+1)*c]) + '\n'
    outs += '\n   ' + IO.spread(ascii_lowercase[:c])
    print(Color.paint(outs))
### end class IO
