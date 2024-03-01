def foo(a,b,c):
  if a==0 and b==0 and c==0: 
    print(0,0,0,-1)
    return -1
  sofar = -1
  for aa in range(0,a):
    sofar = max(sofar, -foo(aa,b,c))
    if sofar==1: 
      print(a,b,c,sofar)
      return sofar
  for bb in range(0,b):
    sofar = max(sofar, -foo(a,bb,c))
    if sofar==1: 
      print(a,b,c,sofar)
      return sofar
  for cc in range(0,c):
    sofar = max(sofar, -foo(a,b,cc))
    if sofar==1: 
      print(a,b,c,sofar)
      return sofar
  print(a,b,c,sofar)
  return sofar

foo(1,1,1)
