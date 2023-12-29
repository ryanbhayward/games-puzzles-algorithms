"""
  for hex and go  rbh 2024
  classes Cell, Color, Game, IO, Point, UF   i
"""

from string import ascii_lowercase

class Game:
  go_game, hex_game = 0, 1

class Cell: ############## board cells ###############
  b, w, e, io_ch = 0, 1, 2, '*@.'  # black, white, empty
  bw = (b, w)

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

  def disp(is_hex, bs, r, c): 
    s = '\n'
    if is_hex: # print hex board
      s += '   ' + IO.spread(ascii_lowercase[:c]) + '\n'
      for y in range(r):
        s += y*' ' + f'{y+1:2}  ' +IO.spread(bs[y*c:(y+1)*c])
        s += ' ' + Cell.io_ch[1] + '\n'
      s += '    ' + ' '*r + (' ' + Cell.io_ch[0])*c
    else:     # print go board
      for y in reversed(range(r)): # print last row first
        s += f'{y+1:2} '+ IO.spread(bs[y*c:(y+1)*c]) + '\n'
      s += '\n   ' + IO.spread(ascii_lowercase[:c])
    print(Color.paint(s, Cell.io_ch))

  def show_blocks(n, stones, parents, blocks, liberties):
    for pcol in Cell.bw:
      print(Cell.io_ch[pcol], 'blocks', end=' ')
      for p in range(n):
        if Pt.point_color(stones, p) == pcol and UF.is_root(parents, p):
          print(blocks[p], end=' ')
      print()
      print(Cell.io_ch[pcol], 'liberties', end=' ')
      for p in range(n):
        if Pt.point_color(stones, p) == pcol and UF.is_root(parents, p):
          print(liberties[p], end=' ')
      print()

  def test():
    print('tests for class IO\n')
    stone_sets = (set(), set())
    stone_sets[0].add(0)
    stone_sets[1].add(1)
    for r in range(2,5):
      for c in range(2,5):
        IO.disp(stone_sets, r, c)

class Pt: ############## board points     ###############

  def rc_point(row, col, num_cols):
    return col + row * num_cols

  def point_color(stones, p):
    if p in stones[Cell.b]: return Cell.b
    if p in stones[Cell.w]: return Cell.w
    return Cell.e

  def show_go_point_names(r, c):  # confirm names look ok
    print('\ngo board point names\n')
    for y in range(r - 1, -1, -1): #print last row first
      for x in range(c):
        print(f'{Pt.rc_point(y, x, c):3}', end='')
      print()

  def show_hex_point_names(r, c):  # confirm names look ok
    print('\nhex board point names\n')
    for y in range(r): #print last row first
      print('  '*y, end='')
      for x in range(c):
        print(f'{Pt.rc_point(y, x, c):4}', end='')
      print()


class UF: ############# simple union/find  ##############

  def union(parents, x, y):
    x = UF.find(parents, x)
    y = UF.find(parents, y)
    parents[y] = x # x is root of merged trees
    return x, y

  def find(parents, x):
    while x != parents[x]:
      x = parents[x]
    return x

  def is_root(parents, p):
    return parents[p] == p

  # if find(   ) becomes a computational bottleneck, use
  #    this grandparent-compression version:
  # def find(parent,x): 
  #   while True:
  #     px = parent[x]
  #     if x == px: return x
  #     gx = parent[px]
  #     if px == gx: return px
  #     parent[x], x = gx, gx

#Cell.test()
#IO.test()
