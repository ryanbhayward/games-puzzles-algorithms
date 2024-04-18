# simple alpha-beta-search demo  rbh 2019 (edits 2024)
from time import sleep
from sys import stdin

def isLeaf(v,V): # V is the set of terminal nodes
  return v in V

def alphabeta(d, T, V, v, alpha, beta): # leaf scores for MAX (root player)
  def off(d):  return d*' .'
  def kind(d): return 'MAX'   if 0==d%2 else 'MIN'

  print(off(d), v, kind(d), end=': ')
  print('?', alpha, beta)
  if isLeaf(v,V):
    val = V[v] 
    print(off(d), v, 'leaf, val',val)
    return val
  if 0 == d%2: # MAX node
    val = float('-inf')
    for c in T[v]:
      ab = alphabeta(d+1, T, V, c, alpha, beta)
      if ab > val: # have improved current mmax value
        alpha, val = ab, ab
        print(off(d+1),c,'now best child of',v, 'alpha', alpha)
      #else:
      # print(off(d+1),c,'not best child of',v, end=': ')
      #print(val, alpha, beta)
      if alpha >= beta:
        print(off(d+1),'prune remaining children of', v)
        break
    print(off(d), v, val, alpha, beta)
    return val
  #else a MIN node
  val = float('inf')
  for c in T[v]:
    ab = alphabeta(d+1, T, V, c, alpha, beta)
    if ab < val:
      beta, val = ab, ab
      print(off(d+1), c,'now best child of',v, 'beta', beta)
    #else:
    #  print(off(d+1), c,'not best child of',v, end=': ') 
    #print(val, alpha, beta)
    if alpha >= beta:
      print(off(d+1),'prune remaining children of', v)
      break
  print(off(d), v, val, alpha, beta)
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
showtree(L,T,V)
alphabeta(0, T, V, root, float('-inf'), float('inf'))
