############## rbh 2024      ###############

from string import ascii_lowercase

############## board cells      ###############

class Cell: 
  e, b, w, io_ch = 0, 1, 2, '.*@'  # empty, black, white

  def ch_to_cell(ch):
    return Cell.io_ch.index(ch)

  def opponent(c): 
    return 3 - c

  def test():
    io_ch = Cell.io_ch
    for ch in io_ch:
      c = Cell.ch_to_cell(ch)
      print(ch, c, io_ch[c])
    print()
    for j in range(1,3):
      print(j, Cell.opponent(j))

############## end Class Cell

class IO:

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])

  def show_board(bs, r, c): 
    outs = '\n'
    for y in range(r):
      outs += f'{y+1:2} '+ spread(bs[y*c:(y+1)*c]) + '\n'
    outs += '\n   ' + spread(ascii_lowercase[:c])
    print(color.paint(outs))

############## end Class IO

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

############## end Class Color

Cell.test()
