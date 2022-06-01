# compute voltage drops top-bottom of H16, so for black.

loops =  100 
# iterations of voltage computation

# 18 nodes in graph after black capture and dead cell removal
Nbrs = [
[1,2,3,4],
[0,4,5],
[0,5,6],
[0,6,7],
[0,1,5,10,13],
[1,2,4,6,10,13],
[2,3,5,7,8],
[3,6,8,9],
[6,7,9,10,11],
[7,8,11,12],
[4,5,8,11,13,14],
[8,9,10,12,14,15],
[9,11,15,16],
[4,5,10,17],
[10,11,17],
[11,12,17],
[12,17],
[13,14,15,16]
]
#Nbrs2 has added the captured cells back in
Nbrs2 = [
[1,2,3,4,5,6],
[0,6],
[0,6],
[0,6,7],
[0,7,8],
[0,8,9],
[0,1,2,3,7,12,15],
[3,4,6,8,12,15],
[4,5,7,9,10],
[5,8,10,11],
[8,9,11,12,13],
[9,10,13,14],
[6,7,10,13,15,16],
[10,11,12,14,16,17],
[11,13,17,18],
[6,7,12,19],
[12,13,19],
[13,14,19],
[14,19],
[15,16,17,18]
]

def update(V,Nbrs):
  for j in range(1,len(Nbrs)-1):
    vsum = 0.0
    for k in Nbrs[j]:
      vsum+= V[k]
    V[j] = vsum/len(Nbrs[j])

def VDrops(V,Nbrs):
  Drops = []
  for j in range(len(Nbrs)-1):
    delta, v = 0.0, V[j]
    for k in Nbrs[j]:
      if V[k] < v:
        delta += v - V[k]
    Drops.append(delta)
  return Drops

def initV(n):
  V = [0.5] * n
  V[0], V[n-1] = 100.0, 0.0
  return V

Nb = Nbrs2
print(Nb)
print('')
Volts = initV(len(Nb))
print(Volts)
print('')

for t in range(loops):
  update(Volts, Nb)
D = VDrops(Volts,Nb)
print(Volts)
print('')
print(D)
