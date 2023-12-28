"""
  simple io for go and hex         rbh 2024
"""

from string import ascii_lowercase

############## board cells      ###############

class Cell: 

  b, w, e, io_ch = 0, 1, 2, '*@.'  # black, white, empty
  stones = (b, w)

  def from_ch(ch): return Cell.io_ch.index(ch)

  def opponent(c): return 1 - c

  #def get_ptm(ch):
  #divide by floor of 32, get player 1 or 2 based on char * or @
  #  return ord(ch) >> 5 

  def test():
    print('tests for class Cell')
    io_ch = Cell.io_ch
    for ch in io_ch:
      c = Cell.from_ch(ch)
      print(ch, c, io_ch[c])
    print()
    for j in range(2):
      print(j, Cell.opponent(j))

############## end Class Cell

class IO:

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])
  
  def point_ch(stone_sets, p):
    if p in stone_sets[0]: return Cell.io_ch[0]
    if p in stone_sets[1]: return Cell.io_ch[1]
    return Cell.io_ch[2]

  def disp(stone_sets, rows, cols): 
    s = '\n   ' + ' '.join([ascii_lowercase[c] for c in range(cols)]) + '\n'
    p =  -1
    for y in range(rows):
      s += '\n' + y*' ' + f'{y+1:2}  ' 
      for c in range(cols):
         p += 1
         s += ' ' + IO.point_ch(stone_sets, p)
      s += ' ' + Cell.io_ch[1]
    s += '\n    ' + ' '*rows + (' ' + Cell.io_ch[0])*cols
    print(Color.paint(s, Cell.io_ch))

  def test():
    print('tests for class IO\n')
    stone_sets = (set(), set())
    stone_sets[0].add(0)
    stone_sets[1].add(1)
    for r in range(2,5):
      for c in range(2,5):
        IO.disp(stone_sets, r, c)

############## end Class IO

class Color:
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

############## end Class Color

#Cell.test()
#IO.test()
