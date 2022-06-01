def foo(a,b,c):
  print(a,b,c)
  if a==0 and b==0 and c==0: 
    return -1
  sofar = -1
  for aa in range(0,a): # aa takes on values >= 0 and <= a-1
    sofar = max(sofar, -foo(aa,b,c))
    if sofar==1: return 1
  for bb in range(0,b):
    sofar = max(sofar, -foo(a,bb,c))
    if sofar==1: return 1
  for cc in range(0,c):
    sofar = max(sofar, -foo(a,b,cc))
    if sofar==1: return 1
  return sofar

print(foo(0,1,8))
