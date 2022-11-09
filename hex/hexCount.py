#!/usr/bin/env python

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def choose(n, k):
    if 0 <= k <= n:
        p = 1
        for t in range(min(k, n - k)):
           p = (p * (n - t)) // (t + 1)
        return p
    else:
        return 0
	
def pascalTriangle(n):
    for x in range(n + 1):
        for y in range(x + 1):
            print(choose(x, y),end='')
        print('')
    print('')

def boardStates(n, k):
#   number of different (up to 180 degree rotation) k-stone nxn hex states
#       can be deduced from the Tromp formulas in Browne's book

#   exact answer if we ignore rotational symmetry:
    xTerm  = choose(n * n, (k + 1) // 2) * choose(n * n - (k + 1) // 2,  k // 2)
#   adjust for symmetry 
    kd4 = k // 4 ; sTerm = 0
    if 0 == k % 4 or \
       1 == k % 4 and 1 == n % 2:
        sTerm = choose(n * n // 2, kd4) * choose(n * n // 2 - kd4, kd4)
    if 3 == k % 4 and 1 == n % 2:
        sTerm = choose(n * n // 2, kd4) * choose(n * n // 2 - kd4, 1 + kd4)
#   each state now counted twice, so ...
    return (xTerm + sTerm) // 2

def uptoStates(n, s):
#   boardStates with at most s stones
    accum = 0
    for k in range(s + 1):
        accum = accum + boardStates(n, k)
    return accum

def upperBound(n):
#   if no limit on relative stone numbers, then each cell empty/black/white
#   divide by two to remove rotational symmetry
    return (3**(n * n) + 1) / 2

def showCounts(n):
    print(n,'x',n, 'Hex states')
    accum = 0
    for k in range(n * n + 1):
        b = boardStates(n, k)
        accum = accum + b
        print(k, k % 4, b)
    print('=', accum)
    print(' ', upperBound(n), '\n')

def nodeCount7x7():
# number of nodes in 7x7 solver recursion tree, cf TCS paper
    return 71405 + 304217 + 1609665 +2114653 + 235797 + 1145199 + 453194 + \
	61252 + 191105 +    2703 + 407737 +  36165 +     197 +   1196 + \
	47688 + 13912 + 14623 + 7364 + 1285 + 118119 + 1162 + \
	164 + 2804 + 1941 + 1225 + 2459 + 4502 + 1192 + \
	136 + 48876 + 991 + 5613 + 15612 + 12448 + 26759 + \
	89 + 90 + 42387 + 405194 + 2248 + 200341 + 46823 + \
	502521 + 1084920 + 213929 + 2564080 + 1718714 + 389754 + 76212

for n in range(1, 11):
    #print n, '\n', 1.0*uptoStates(n, n*n/2), '\n', uptoStates(n, n*n), '\n', upperBound(n), '\n'
    #print n, '\n', 1.0*uptoStates(n, n*n/2)
    #print n, '\n', uptoStates(n, n*n/2)
    print(n, '\n', uptoStates(n, n*n))
    print( '')

print('7x7 node count', nodeCount7x7())
#for x in range(7):
	#print 'full board states', x,'x',x,' board: ',boardStates(x,x*x)

#for k in range(1,5):
  #print k, boardStates(2,k)
