# chomp solver    RBH 2019
import numpy as np
import copy

# chomp move: remove above and to the right
# position representation: list (topdown) of row lengths,
#    so must be nondecreasing

# convert position to string, for pretty output
# e.g.  (1,3)   =>   x         
#                    x x x
def psn_to_str(L):
  s = ''
  for j in L:
    s += 'x '*j + '\n'
  return s

# return equivalent flipped position
def flip(L):
  rows = len(L)
  f = L[-1]*[1]             # last row has this many columns
  for j in range(len(L)-1): # update column lengths
    for k in range(L[j]):
      f[rows-k] += 1
  return f        # nondecreasing lengths of cols

# make a move at row r, col c, and return new psn
def chomp(L,r,c):
  #if r>len(L) or c>L[r-1]: print(L, r, c)
  assert(r <= (len(L)) and (c <= L[r-1]))
  M = copy.deepcopy(L)
  for j in range(r):
    M[j] = min(M[j], c-1)
  while (len(M)>=1) and (M[0] == 0):
    M.pop(0)
  return M

def options(L): # return non-empty move options from psn L
  Z = []
  rows = len(L)
  for j in range(rows):
    for k in range(L[j]):
      Y = chomp(L,j+1,k+1)
      if len(Y)>0: Z.append(Y)
  return Z

def promote(L,w):    # replace L with its successor
  n = len(L)
  j = n - 1
  while j>=0 and L[j] == w: 
    j -= 1
  if j<0:
    for j in range(n): 
      L[j] = 1
    L.append(1)
  else:
    L[j]+= 1
    for k in range(j+1,n):
      L[k] = L[j]

# L1 L2 ... Lt  =>  L1*n^(t-1) + ... + Lt*n^0
# TODO: there are better hash functions ...
#   many sequences are illegal and so not used
#   e.g. can represent a position as list with
#     - 1st row length, followed by vector of deltas
#     - e.g. 1 1 2 4 5  =>  1 0 1 2 1
#     - sum of entries is at most width of board
#   e.g. can represent a position as path along 
#        top edge, each step is either right or down,
#        so 2^(m+n) possible sequences
def myhash(L,n):          # n is max row length
  assert(len(L)<=n)
  h, m = 0, 1
  for j in L:
    assert((0 < j) and (j <= n))
    h += m*j
    m *= (n+1)
  return h

def tst():
  for L in [[1], [3], [1,1,2,5]]:
    print(L)
    print(psn_to_str((L)))
    print(myhash(L,5))
    F = flip(L)
    print(psn_to_str(F))
    print(myhash(F,5))

tst()

#L = [1,2,3]
#print(chomp(L,1,1))
#print(chomp(L,2,1))
#print(chomp(L,2,2))
#print(chomp(L,3,1))
#print(chomp(L,3,2))
#print(chomp(L,3,3))
print(options([1,2,3]))

#Ppsns = set([1])
#print(Ppsns)
#for j in range(3):
  #if j in Ppsns: print(j)
  #else: print('no')

def is_rect(L):
  n = len(L)
  if n == 1: 
    return True
  for j in range(1,n):
    if L[j] != L[0]: 
      return False
  return True

def ppsns(rows,cols):
  L = [1]
  r,c = rows, cols
  while len(L) < rows+1:
    print('psn')
    print(L)
    if is_rect(L): print('      rect')
    else:          print('       not')
    #print('options')
    #print(options(L))
    #print('')
    promote(L, cols)

ppsns(3,3)

#L = [1,2,3]
#for t in range(10):
  #promote(L,5)
  #print(L)
