# starting from root, count paths in the trigo transition digraph
# rbh 2024

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

def clear_color(p, ch):
  s = ''
  for c in p:
    if c == ch: s += '.'
    else: s += c
  return s

def opponent(c):
  if c == 'x': return 'o'
  if c == 'o': return 'x'

class Graph:
  colors = '.xo'
  psns = [] # each node is a trigo position
  nbrs = {} # dictionary: psn -> neighbors

  def children(self, brd, color):
    kids = []
    pc = brd.count(color)
    oc = brd.count(opponent(color))
    assert(pc + oc != 3)
    if pc + oc <= 1:
      for j in (0,1,2):
        if brd[j] == self.colors[0]:
          new = change_string(brd, j, color)
          kids.append(new)
    else:
      assert(pc + oc == 2)
      if pc <= 1:
        for j in (0,1,2):
          if brd[j] == self.colors[0]:
            new = change_string(brd, j, color)
            new2 = clear_color(new, opponent(color))
            kids.append(new2)
    return kids

  def show_nbrs(self):
    for p in self.nbrs: 
      print(p, ': ', end='')
      for v in self.nbrs[p]:
        print(v, end=' ')
      print()

  def __init__(self):
    for a in self.colors:
      for b in self.colors:
        for c in self.colors:
          p = a+b+c
          if self.colors[0] in p:
            self.psns.append(p)
    self.psns.sort()
    for p in self.psns: 
      self.nbrs[p] = set()
      for clr in 'xo':
        kids = self.children(p, clr)
        for k in kids:
          self.nbrs[p].add(k)

  def explore(self, path):
    global count
    if len(count) < len(path):
      assert(len(count) == len(path) - 1)
      count.append(0)
    count[len(path) - 1] += 1

    for v in self.nbrs[path[-1]]:
      if v not in path:
        path.append(v)
        self.explore(path)
        path.pop()

    if len(path) == 1: 
      print('\n nodes ', sum(count))
      print(' depth')
      for j in range(len(count)):
        print('  {:2d}'.format(j), '    {:3d}'.format(count[j]))
      print()

g = Graph()
count = []
path = ['...']
g.explore(path)
g.show_nbrs()
