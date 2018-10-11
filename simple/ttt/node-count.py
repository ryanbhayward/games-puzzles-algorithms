# upper bound on number of nodes in ttt search tree

def fallfac(n,k):
  p = 1
  for j in range(k):
    p *= n-j
  return p

def nodes():
  s = 1
  for j in range(9):
    s +=  fallfac(9, j+1)
  return s
  
for j in range(9):
  print(j, fallfac(9,j+1))

print(nodes())
