def fib(n):
  if n<=1: 
    return n
  return fib(n-2)+fib(n-1)

for j in range(40):
  print(j, fib(j))
