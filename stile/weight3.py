# converted to python 3
# used for weighted graphs
from sys import stdin
from re import findall
def weightSum(G):
  sum = 0
  for u in G: 
    for (v,weight) in G[u]: sum += weight
  return sum

def infinity(G): return 999+weightSum(G)

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

G355 = {'A': [['S',140],['T',118],['Z',75]],
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
#Gtest = readWGraph()
#print(Gtest)
#showGraph(Gtest)
