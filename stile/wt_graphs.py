# converted to python 3
# used for weighted graphs
from sys import stdin
from re import findall

def weightSum(G):
  sum = 0
  for u in G: 
    for (v,weight) in G[u]: sum += weight
  return sum

def indexOfMin(L,C):
  ndx = 0
  for j in range(1,len(L)):
    if C[L[j]] < C[L[ndx]]: ndx = j
  return ndx

def showAll(G,D,P):
  print('\nprnt', end='')
  for v in sorted(G): print(P[v], end='')
  print('\nnode', end='')
  for v in sorted(G): print(v, end='')
  print('\ncost', end='')
  for v in sorted(G): print(D[v], end='')
  print('')

def showFringe(G,F,D,inf):
  print('  fringe', end='')
  for v in sorted(F):
    if D[v]!=inf:
      print(v,D[v],' ', end='')

def readWGraph():
  G = {}
  for line in stdin:
    tokens =  findall(r"[^\W\d_]+|\d+", line)
    if len(tokens)>0:
      node = tokens.pop(0)
      nbrs = []
      while len(tokens)>0: 
        nbrs.append([tokens.pop(0), int(tokens.pop(0))])
    G[node] = nbrs
  return G

def showGraph(G):
  print('{')
  for node in sorted(G):
    print('\''+node+'\':',G[node],',')
  print('}')

def nodeList(G):
  L = [x for x in G]
  print(L)
  return L

wg_355 = {'A': [['S',140],['T',118],['Z',75]],
        'B': [['F',211],['P',101]],
        'C': [['D',120],['P',138],['R',145]],
        'D': [['C',120],['M',75]],
        'F': [['B',211],['S',99]],
        'L': [['M',70],['T',111]],
        'M': [['D',75],['L',70]],
        'P': [['B',101],['C',138],['R',97]],
        'Q': [['S',151],['Z',71]],
        'R': [['C',145],['P',97],['S',80]],
        'S': [['A',140],['F',99],['Q',151],['R',80]],
        'T': [['A',118],['L',111]],
        'Z': [['A',75],['Q',71]]
}
wg_pq2 = {'A': [['B',20],['C',10]],
          'B': [['A',20],['Z',20]],
          'C': [['A',10],['Z',23]],
          'Z': [['B',20],['C',23]]
}
wg_pq = {'A': [['B',10],['D',15]],
         'B': [['A',10],['C',10]],
         'C': [['B',10],['F',21]],
         'D': [['A',15],['E',12]],
         'E': [['D',12],['G',15]],
         'F': [['C',21],['Z', 8]],
         'G': [['E',15],['Z',10]],
         'Z': [['F', 8],['G',10]]
}

h_pq =  [28, 26, 24, 22, 18, 7, 10, 0]
h_pq2 = [28, 20, 22, 0]
h_355 = [366, 0, 160, 242, 176, 244, 241, 100, 380, 193, 253, 329, 374]

#Gtest = readWGraph()
#print(Gtest)
#showGraph(Gtest)

#              [  0, 26, 24, 22, 18,  7, 10, 0 ]
  #              [  0, 26, 25, 20, 17,  7, 10, 0 ]
  #              [  0, 26, 24, 22, 18,  7,  2, 0 ]
  #              [  0, 26, 25, 22, 17,  7,  2, 0 ]
  #              [  0, 26, 24, 22,  2,  7, 10, 0 ]
  #nodes, hvals = ['A','B','C','D','E','F','G','Z'],\
  #               [  0, 26, 25, 22,  2,  7, 10, 0 ]
