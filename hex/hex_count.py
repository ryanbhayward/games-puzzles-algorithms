# upper bound on number of hex positions reachable from empty board
#   * ignore symmetry
#   * ignore positions when game already ended
# revised 2024 rbh
#   todo
#     * count true reachable (stop once game ends)
#     * also consider symmetry (see dev)

from math import comb, floor, ceil

def board_states(n, k):
  s1, s2 = ceil(k/2), floor(k/2) # number of stones for players 1 and 2
  return comb(n*n, s1) * comb(n*n - s1, s2)

def upto_states(n, s): #   board_states with at most s stones
    return sum([board_states(n,k) for k in range(s+1)])

def power3(n):
#   if no limit on relative stone numbers, then each cell empty/black/white
    return (3**(n * n))

def show(n):
    print('\n hex ',n, 'x', n,' board', sep='')
    #for k in range(n*n+1):
    #  print('  ', k, 'stones', board_states(n, k))
    psns, pow3 = upto_states(n, n*n), power3(n)
    print(' positions', psns)
    print(' ^3-bound ', pow3)
    print('ratio', psns/pow3)

def nodeCount7x7():
# number of nodes in 7x7 solver recursion tree, cf TCS paper
    return 71405 + 304217 + 1609665 +2114653 + 235797 + 1145199 + 453194 + \
	61252 + 191105 +    2703 + 407737 +  36165 +     197 +   1196 + \
	47688 + 13912 + 14623 + 7364 + 1285 + 118119 + 1162 + \
	164 + 2804 + 1941 + 1225 + 2459 + 4502 + 1192 + \
	136 + 48876 + 991 + 5613 + 15612 + 12448 + 26759 + \
	89 + 90 + 42387 + 405194 + 2248 + 200341 + 46823 + \
	502521 + 1084920 + 213929 + 2564080 + 1718714 + 389754 + 76212

for n in range(1,7):
    show(n)
