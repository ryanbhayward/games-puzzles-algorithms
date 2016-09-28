# simple alpha-beta-search demo  rbh 2016
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
  return L,T,V

def showtree(L,T,V):
  for v in sorted(L):
    print(v, end=' ')
    if (v in T and len(T[v])>0):
      print(T[v], end=' ')
    if v in V:
      print(V[v], end=' ')
    print('')
  print('')

def alphabetanega(d, T, V, v, alpha, beta):
# assume leaf scores are for root player
  def showdata():
    sleep(.5)
    for j in range(d): print('  ',end='')
    print(v, alpha, beta, so_far)

  so_far = NEGINF  # best score so far
  showdata()
  if v in V: # all leaves are in V
  #if len(T[v])==0: # v has no children
    # convert to score for player to move, so
    # if odd depth, negate score
    if 0==d%2: return  V[v]
    else:      return -V[v]
  for c in T[v]:
    so_far = max(so_far, -alphabetanega(d+1,T,V,c, -beta, -alpha) )
    alpha = max(alpha, so_far)
    if alpha >= beta:
      print('         cutoff')
      break
  showdata()
  return so_far

L,T,V = readtree()
showtree(L,T,V)
alphabetanega(0, T, V, 'A', NEGINF, INF)
