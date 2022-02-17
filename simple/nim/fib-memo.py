'''
recursive fibonacci, with memoization:
  avoid recomputation with a dictionary
'''

fib_values = {0:0, 1:1} 

def fib(n, D):
  if n <= 1:
    return n
  f = [0, 0]
  for j in range(1,3):
    if n - j in D:
      f[j - 1] = D[n - j]
    else:
      f[j - 1] = fib(n - j, D)
      D[n - j] = f[j - 1]   # what happens if you forget this line?
  return sum(f)

for j in range(40):
  print(j, fib(j, fib_values))
