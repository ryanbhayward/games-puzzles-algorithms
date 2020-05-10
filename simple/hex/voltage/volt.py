from fractions import Fraction
# compute voltage drops across empty hex board, with 1.0 on top and 0.0 on bottom
# remove connection between adjacent cells in first and last row, as
#   these are not in any minimal winning path
# notice that node with biggest voltage drop is 2,2, not center :)

slim, n = True, 2
assert(n>1)
nsq = n*n

Voltages = [0.5] * nsq
#print(Voltages)

Nbrs = []
for j in range(nsq):
  UL,UR,L,R,DL,DR = j-n, 1+j-n, j-1, j+1, j+n-1, j+n # up left, up right, ...
  if j==0:
    if slim: Nbrs.append([DR])
    else:    Nbrs.append([DR,R])
  elif j==nsq-1:
    if slim: Nbrs.append([UL])
    else:    Nbrs.append([UL,L])
  elif j==n-1:
    if slim: Nbrs.append([DL,DR])
    else:    Nbrs.append([DL,DR,L])
  elif j== nsq-n:
    if slim: Nbrs.append([UR,UL])
    else:    Nbrs.append([UR,UL,R])
  elif j<n:
    if slim: Nbrs.append([DL,DR])
    else:    Nbrs.append([DL,DR,L,R])
  elif j>=nsq-n:
    if slim: Nbrs.append([UR,UL])
    else:    Nbrs.append([UR,UL,R,L])
  elif 0 == j%n:
    Nbrs.append([UL,UR,R,DR])
  elif n-1 == j%n:
    Nbrs.append([DR,DL,L,UL])
  else:
    Nbrs.append([UL,UR,L,R,DL,DR])

def show(X,n):
  print('')
  for j in range(n):
    for k in range(n):
      print X[n*j+k],
    print('')

def flipshow(X,n):
  print('')
  for k in range(n):
    for j in range(n):
      print int(round(100.0*X[n*j+k])),
    print('')

def update(V,N,n):
  for j in range(n*n):
    if j < n:
      v,c = 1.0, 1  # implicit nbr at top, voltage 1.0
    elif j >= n*n-n:
      v,c = 0.0, 1  # implicit nbr at bottom, voltage 0.0
    else:
      v,c = 0.0, 0  
    for k in N[j]:
      v+= V[k]
      c += 1
    V[j] = v/c

def VDrops(V,Nbrs,n):
  Drops = []
  #for j in range(n):
  #  Drops.append(1.0-V[j])
  #for j in range(n,n*n):
  for j in range(n*n):
    delta, v      = 0.0, V[j]
    if j<n: delta = 1.0-V[j]   # implicit nbr
    for k in Nbrs[j]:
      if V[k] > v:
        delta += V[k] - v
    Drops.append(delta)
  return Drops

#show(Nbrs,n)
for t in range(3**n):
  update(Voltages, Nbrs, n)
#show(Voltages,n)
flipshow(Voltages,n)
#for d in Voltages:
  #print(d, Fraction.from_float(d).limit_denominator(99999999))
D = VDrops(Voltages,Nbrs,n)
show(D,n)
flipshow(D,n)
