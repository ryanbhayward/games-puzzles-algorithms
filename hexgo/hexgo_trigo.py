"""
  for trigo  rbh 2024
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

  def disp(bs): 
    print(Color.paint('\n' + bs, Cell.io_ch))

  def test():
    print('tests for class IO\n')
    stone_sets = (set(), set())
    stone_sets[0].add(0)
    stone_sets[1].add(1)
    for j in (0,1): print(stone_sets[j])

class Pt: ############## board points     ###############

  def point_color(stones, p):
    if p in stones[Cell.b]: return Cell.b
    if p in stones[Cell.w]: return Cell.w
    return Cell.e

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

  def in_same_block(parents, x, y):
     return UF.find(parents, x) == UF.find(parents,y)

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
