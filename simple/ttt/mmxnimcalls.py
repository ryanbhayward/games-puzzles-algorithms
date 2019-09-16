def foo(a,b,c):
  if a==0 and b==0 and c==0: return 1
  ttl = 1
  for aa in range(0,a): ttl += foo(aa,b,c)
  for bb in range(0,b): ttl += foo(a,bb,c)
  for cc in range(0,c): ttl += foo(a,b,cc)
  return ttl

print(foo(0,1,2))
