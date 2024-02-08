# simple negamax   rbh 2024
from sys import stdin

NEGINF = -999

def isTerminalNode(v,V): # V is the set of terminal nodes
  return v in V

def negamax(d, T, V, v): # leaf scores for player-to-move
  print(d*'  ', v)
  if isTerminalNode(v,V): 
    val = V[v]; print(d*'  ', v, 'leaf', val); return val
  val = NEGINF
  for c in T[v]:
    val = max(val, -negamax(d+1, T, V, c))
  print(d*'  ', v, val)
  return val

def readtree():
# L   labels,  ie. single-character node names
# T   nbr lists of          all non-leaf nodes
# V   root-player-minimax-values of all leaves
  lines = []
  for line in stdin:
    if line[0] != '#':
      lines.append(line.strip())
  L = []
  for c in lines[0]: # get labels (node names)
    L.append(c)
  T,V = {}, {}
  for j in range(1,len(lines)):
    row = lines[j].split()
    node = row[0][0]
    if len(row[0]) > 1:
      assert(len(row)==2)
      assert(row[0][1]==':')
      nbrs = []
      for c in row[1]:
        nbrs.append(c)
      T[node] = nbrs
    else:
      V[node] = int(row[1])
  for node in V:
    assert(node not in T)
  for node in T:
    for nbr in T[node]:
      assert(nbr in T or nbr in V)
  return L,T,V, L[0]

def showtree(L,T,V):
  print('showtree')
  for v in sorted(L):
    print(v, end=' ')
    if (v in T and len(T[v])>0): 
      print(T[v], end=' ')
    if v in V:  
      print(V[v], end=' ')
    print('')
  print('')

L,T,V,root = readtree()
#showtree(L,T,V)
negamax(0, T, V, root)
