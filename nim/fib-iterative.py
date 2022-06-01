'''
iterative fibonacci, with remembering
'''

def fib(n):
  F = [0,1]
  for j in range(2,n+1):
    F.append(F[j-1] + F[j-2])
  return F[n]

for j in range(41):
  print(j, fib(j))
