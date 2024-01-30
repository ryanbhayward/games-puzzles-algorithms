# simple astar 
import weight3
def astar(G,source, target):
  def show_nodes(n, nodes):
    print('\n ', end='')
    for j in range(n):
      print(nodes[j], end='   ')
    print()

  def show_heur(n, heur):
    for j in range(n): 
      print('{:3d}'.format(heuristic[nodes[j]]), end=' ')
    print()

  def show_vals(G, vals, infty):
    for v in G:
      print('{:3d}'.format(vals[v]) if vals[v]<infty else '---', end=' ')
    print()

  def show_done(G, done):
    for v in G:
      print('xxx' if v in done else '   ', end=' ')
    print()
    
  infty = weight3.infinity(G)
  dist, priority, heuristic, parent, fringe, done = {}, {}, {}, {}, [], []
  for v in G:
    dist[v], priority[v], parent[v] = infty, infty, -1
  dist[source], priority[source], parent[source] = 0, 0, source

  #nodes, hvals = ['A','B','C','Z'], [0, 20, 22, 0]
  #              [  0, 26, 24, 22, 18,  7, 10, 0 ]
  #              [  0, 26, 25, 20, 17,  7, 10, 0 ]
  #              [  0, 26, 24, 22, 18,  7,  2, 0 ]
  #              [  0, 26, 25, 22, 17,  7,  2, 0 ]
  #              [  0, 26, 24, 22,  2,  7, 10, 0 ]
  #nodes, hvals = ['A','B','C','D','E','F','G','Z'],\
  #               [  0, 26, 25, 22,  2,  7, 10, 0 ]
  nodes, hvals = ['A','B','C','D','F','L','M','P','Q','R','S','T','Z'],\
                 [366, 0, 160,242,176,244,241,100,380,193,253,329,374]
  n = len(nodes)
  assert n==len(hvals)
  for j in range(n): 
    heuristic[nodes[j]] = hvals[j]
  show_nodes(n, nodes)
  show_heur(n, heuristic)

  msg = '*'
  fringe.append(source)
  while len(fringe) > 0:
    current = fringe.pop(weight3.indexOfMin(fringe, priority))
    done.append(current)
    print('\n', current, 'done: dist-from-source', dist[current], 'est-total', priority[current], '\n')
    msg = msg + current + '*' + str(priority[current]) + '*'
    if current == target: break
    for (v, wuv) in G[current]:
      if v not in done:
        new_v_dist = dist[current] + wuv
        if new_v_dist < dist[v]:
          dist[v] = new_v_dist
          parent[v] = current
          priority[v] = new_v_dist + heuristic[v]
          if v not in fringe: fringe.append(v)
    show_nodes(n, nodes)
    show_heur(n, heuristic)
    show_vals(G, dist, infty)
    show_done(G, done)
    show_vals(G, priority, infty)
  print(msg)
  print('')

#G = weight3.G8
G = weight3.G355
#print(G)
astar(G,'A','B')
# 
