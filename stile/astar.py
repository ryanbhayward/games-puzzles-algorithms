# simple astar 
import weight3
from time import sleep
from math import inf

def astar(G,source, target):
  def show_nodes(n, nodes):
    print('\n ', end='')
    for j in range(n):
      print(nodes[j], end='   ')
    print()

  def show_heur(n, heur):
    for j in range(n): 
      print('{:3d}'.format(heurstc[nodes[j]]), end=' ')
    print()

  def show_vals(G, vals):
    for v in G:
      print('{:3d}'.format(vals[v]) if vals[v] < inf else 'inf', end=' ')
    print()

  def show_done(G, done):
    for v in G:
      print('xxx' if v in done else '   ', end=' ')
    print()
    
  dist, priority, heurstc, parent, fringe, done = {}, {}, {}, {}, [], []
  for v in G:
    dist[v], priority[v], parent[v] = inf, inf, -1
  dist[source], priority[source], parent[source] = 0, 0, source

  nodes, hvals = ['A','B','C','Z'], [30, 20, 23, 0]
  #              [  0, 26, 24, 22, 18,  7, 10, 0 ]
  #              [  0, 26, 25, 20, 17,  7, 10, 0 ]
  #              [  0, 26, 24, 22, 18,  7,  2, 0 ]
  #              [  0, 26, 25, 22, 17,  7,  2, 0 ]
  #              [  0, 26, 24, 22,  2,  7, 10, 0 ]
  #nodes, hvals = ['A','B','C','D','E','F','G','Z'],\
  #               [  0, 26, 25, 22,  2,  7, 10, 0 ]
  #nodes, hvals = ['A','B','C','D','F','L','M','P','Q','R','S','T','Z'],\
  #               [366, 0, 160,242,176,244,241,100,380,193,253,329,374]
  n = len(nodes)
  assert n==len(hvals)
  for j in range(n): 
    heurstc[nodes[j]] = hvals[j]
  show_nodes(n, nodes)
  show_heur(n, heurstc)

  msg = '*'
  fringe.append(source)
  while len(fringe) > 0:
    node = fringe.pop(weight3.indexOfMin(fringe, priority))
    done.append(node)
    print('\n', node, 'done: d-from-source', dist[node], 'est-total', priority[node], '\n')
    msg = msg + node + '*' + str(priority[node]) + '*'
    if node == target: break
    for (v, wuv) in G[node]:
      if v not in done:
        new_v_dist = dist[node] + wuv
        if new_v_dist < dist[v]:
          dist[v] = new_v_dist
          parent[v] = node
          priority[v] = new_v_dist + heurstc[v]
          if v not in fringe: fringe.append(v)
    #show_nodes(n, nodes)
    #show_heur(n, heurstc)
    show_vals(G, dist)
    show_done(G, done)
    show_vals(G, priority)
  print('msg', msg)
  print('')

G = weight3.PQ2
astar(G,'A','Z')
#G = weight3.G355
#print(G)
#astar(G,'A','B')
