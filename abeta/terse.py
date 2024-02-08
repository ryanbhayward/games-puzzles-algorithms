# simple alpha-beta-search demo  rbh 2019
from time import sleep
from sys import stdin

NEGINF, INF = -999, 999

def isTerminalNode(v,V): # V is the set of terminal nodes
  return v in V

def isMaxNode(v, d): # in our examples, terminal iff even depth
  return 0 == d % 2

def alphabeta(d, T, V, v, alpha, beta): # leaf scores for MAX (root player)
  print(d*'  ', v,'MAX' if isMaxNode(v,d) else 'MIN','?',alpha,beta)
  if isTerminalNode(v,V): val = V[v]; return val
  if isMaxNode(v, d):
    val = NEGINF
    for c in T[v]:
      ab = alphabeta(d+1, T, V, c, alpha, beta)
      if ab > val: alpha, val = ab, ab
      if alpha > beta: 
        print((d+1)*'  ','prune rem. ch. of', v); break
    print(d*'  ', v, val, alpha, beta)
    return val
  val = INF
  for c in T[v]:
    ab = alphabeta(d+1, T, V, c, alpha, beta)
    if ab < val: beta, val = ab, ab
    if alpha > beta: 
      print((d+1)*'  ','prune rem. ch. of', v); break
  print(d*'  ', v, val, alpha, beta)
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
alphabeta(0, T, V, root, NEGINF, INF)
