# simple alpha-beta-search demo  rbh 2019
from time import sleep
from sys import stdin

NEGINF, INF = -999, 999

def readtree():
# L   labels,  ie. single-character node names
# T   nbr lists of          all non-leaf nodes
# V   root-player-minimax-values of all leaves
  lines = []
  for line in stdin:
    if line[0] != '#':
      lines.append(line.strip())
  L = []
  # get labels, ie. node names
  for c in lines[0]:
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
  for v in sorted(L):
    print(v, end=' ')
    if (v in T and len(T[v])>0): print(T[v], end=' ')
    if v in V:                   print(V[v], end=' ')
    print('')
  print('')

def alphabeta(d, T, V, v, alpha, beta): # leaf score are for root player: MAX
  print(d*'  ', v, 'max' if 0==d%2 else 'min')
  print(d*'  ', '?', alpha, beta)
  if v in V: # V is set of leaves
    val = V[v]; print(d*'  ', 'leaf value',val)
    return val
  if 0 == d%2: # d is even, a MAX node
    val = NEGINF
    for c in T[v]:
      ab = alphabeta(d+1, T, V, c, alpha, beta)
      if ab > val:
        alpha, val = ab, ab
        print((d+1)*'  ',c,'new best child of',v)
      else:
        print((d+1)*'  ',c,'not best child of',v)
      print((d+1)*'  ', val, alpha, beta)
      if alpha >= beta:
        print((d+1)*'  ','alpha >= beta, prune remaining children of', v)
        break
    print(d*'  ', v, 'done')
    print(d*'  ', val, alpha, beta)
    return val
  else: # d is odd, a MIN node
    val = INF
    for c in T[v]:
      ab = alphabeta(d+1, T, V, c, alpha, beta)
      if ab < val:
        beta, val = ab, ab
        print((d+1)*'  ', c,'new best child of',v)
      else:
        print((d+1)*'  ', c,'not best child of',v) 
      print((d+1)*'  ', val, alpha, beta)
      if alpha >= beta:
        print((d+1)*'  ','alpha >= beta, prune remaining children of', v)
        break
    print(d*'  ', v, 'done')
    print(d*'  ', val, alpha, beta)
    return val

L,T,V,root = readtree()
showtree(L,T,V)
alphabeta(0, T, V, root, NEGINF, INF)
