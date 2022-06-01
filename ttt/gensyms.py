# for 3x3 ttt board,
#   generate list of positions of symmetry group
#   generate list of winning lines
# I printed output, then copy/pasted into main program

from itertools import product
rows, cols = [0,1,2], [0,1,2]

def getnextperms(L, r, c):
  perm = []
  for j in product(r,c): 
    perm.append(j)
  L.append(perm)
  perm = []
  for j in product(r,c): 
    perm.append(j[::-1])
  L.append(perm)

M = []
getnextperms(M, rows, cols)
cols.reverse()
getnextperms(M, rows, cols)
rows.reverse()
getnextperms(M, rows, cols)
cols.reverse()
getnextperms(M, rows, cols)
#for t in M: print(t)

win_lines = []
for r in range(3):
  # winning row
  x = []
  for c in range(3):
    x.append((r,c))
  win_lines.append(x)
  # winning col
  x = []
  for c in range(3):
    x.append((c,r))
  win_lines.append(x)
# winning diagonals
x,y = [], []
for r in range(3):
  x.append((r,r))
  y.append((r,2-r))
win_lines.append(x)
win_lines.append(y)

for w in win_lines:
  print(w,',')
