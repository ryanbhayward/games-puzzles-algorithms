# simple astar 
import weight3
from time import sleep
from math import inf
PAUSE  = 1
DSF, ETD = 0, 1

def astar(G, source, target):
  def welcome():
    print('\n A-star road-map demo\n'); sleep(PAUSE)
    print(' DSF  distance so far'); sleep(PAUSE)
    print(' ERD  est. remaining distance (heuristic)'); sleep(PAUSE)
    print(' ETD  est.   total   distance (DSF + ERD)\n'); sleep(PAUSE)
    print('     here ERD is crow-flies distance, never more'); sleep(PAUSE)
    print('       than road distance, so heur. admissable,'); sleep(PAUSE)
    print('       so DSF values are shortest distances'); sleep(PAUSE)
   
  def show_nodes(n, nodes):
    print('\n nodes   ', end='')
    for j in range(n):
      print(nodes[j], end='   ')
    print(); sleep(PAUSE)

  def show_heur(n, heur):
    print(' ERD   ', end='')
    for j in range(n): 
      print('{:3d}'.format(heurstc[nodes[j]]), end=' ')
    print('\n'); sleep(PAUSE)

  def show_vals(G, vals, kind):
    if kind == DSF: 
      print(' DSF   ', end='')
    else:
      print(' ETD   ', end='')
    for v in G:
      print('{:3d}'.format(vals[v]) if vals[v] < inf else 'inf', end=' ')
    print(); sleep(PAUSE)

  def show_done(G, done):
    print('done?   ', end='')
    for v in G:
      print('yes' if v in done else '   ', end=' ')
    print('\n'); sleep(PAUSE)
    
  dist, etd, heurstc, parent, fringe, done = {}, {}, {}, {}, [], []
  for v in G:
    dist[v], etd[v], parent[v] = inf, inf, -1
  dist[source], etd[source], parent[source] = 0, 0, source

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

  welcome()

  n = len(nodes)
  assert n==len(hvals)
  for j in range(n): 
    heurstc[nodes[j]] = hvals[j]
  show_nodes(n, nodes)
  show_heur(n, heurstc)

  msg = ''
  fringe.append(source)
  while len(fringe) > 0:
    node = fringe.pop(weight3.indexOfMin(fringe, etd))
    done.append(node)
    show_vals(G, dist, DSF)
    show_vals(G, etd, ETD)
    show_done(G, done)
    if len(msg)>0: 
      msg += ', '
    msg = msg + node + ' ' + str(etd[node])
    if node == target: break
    for (v, wuv) in G[node]:
      if v not in done:
        new_v_dist = dist[node] + wuv
        if new_v_dist < dist[v]:
          dist[v] = new_v_dist
          parent[v] = node
          etd[v] = new_v_dist + heurstc[v]
          if v not in fringe: fringe.append(v)
  print(' distances, in order found:\n  ', msg)

G = weight3.PQ2
astar(G,'A','Z')
#G = weight3.G355
#print(G)
#astar(G,'A','B')
