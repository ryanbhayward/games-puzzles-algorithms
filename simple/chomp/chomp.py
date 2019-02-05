# chomp solver    RBH 2019
import numpy as np
import copy

# convert chomp position, as list of row-lengths, to string
#  (1,3) = > x         
#            x x x
def psn_to_str(L):
  s = ''
  for j in L:
    s += 'x '*j + '\n'
  return s

def flip(L):
  f = L[-1]*[1]
  for j in range(len(L)-1):
    for k in range(L[j]):
      f[k] += 1
  return f

def chomp(L,r,c):
  assert(r <= (len(L)) and (c <= L[r-1]))
  M = copy.deepcopy(L)
  for j in range(r):
    M[j] = min(M[j], c-1)
  while (len(M)>=1) and (M[0] == 0):
    M.pop(0)
  return M

# list of all non-empty move options from L
def options(L):
  Z = []
  for j in L:
    for k in range(j):
      Y = chomp(L,j,k+1)
      if len(Y)>0: Z.append(Y)
  return Z

def myhash(L,n):
  assert(len(L)<=n)
  h, m = 0, 1
  for j in L:
    assert((0 < j) and (j <= n))
    h += m*j
    m *= n
    print(j,h)
  return h

for L in [[1], [2], [3], [1,1], [1,2], [1,2,3]]:
  print(L)
  print(myhash(L,3))
  print(flip(L))
  print(myhash(L,3))
  print(psn_to_str((L)))

L = [1,2,3]
print(chomp(L,1,1))
print(chomp(L,2,1))
print(chomp(L,2,2))
print(chomp(L,3,1))
print(chomp(L,3,2))
print(chomp(L,3,3))
print(options([1,2,3]))

Ppsns = set([1])
print(Ppsns)

for j in range(3):
  if j in Ppsns: print(j)
  else: print('no')


