# simple alpha-beta-search demo  rbh 2016  (edits 2024)
# ** this code emits comments to help user understand
# **   the alphabeta (negamax version) algorithm ...
# ** code could be simplified if comments not wanted
from time import sleep
from sys import stdin

def abnega(d, Tree, V, v, alpha, beta): #leaf scores for root player
  def off(d):  return d*' .'
  def ab(d):   return 'alpha' if 0==d%2 else 'beta'
  def kind(d): return 'MAX'  if 0==d%2 else 'MIN'
  def showdata(): print(off(d), v, kind(d), alpha, beta, so_far)
  def leafval(v, V, d): return V[v] if 0==d%2 else -V[v]

  so_far = float('-inf')  # best score so far
  showdata()

  if v in V: # leaves
    # leaf scores are for first player,
    # need to convert for player-to-move:
    # *** val needed only if we want to print comment
    #if 0==d%2: val = V[v]  # even depth, no change
    #else:      val = -V[v]  # odd depth, negate score
    val = leafval(v, V, d)
    print(off(d), v,'leaf',val)
    return val
  for c in Tree[v]:
    # if no comment needed, use following line instead
    # so_far = max(so_far,-abnega(d+1,T,V,c, -beta, -alpha))
    cval = -abnega(d+1,Tree,V,c, -beta, -alpha)
    if cval > so_far:
      print(off(d+1), c,'now', v, "'s best child")
      so_far = cval
    # if no comment needed, use following line instead
    # alpha = max(alpha, so_far)
    if so_far > alpha:
      alpha = so_far
      print(off(d+1), c, ab(d), 'at', v,'now', alpha)
    if alpha >= beta:
      print(off(d+1), 'prune remaining children of', v)
      break
  showdata()
  return so_far

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
    if (v in T and len(T[v])>0):
      print(T[v], end=' ')
    if v in V:
      print(V[v], end=' ')
    print('')
  print('')

L,T,V,root = readtree()
showtree(L,T,V)
abnega(0, T, V, root, float('-inf'), float('inf'))
