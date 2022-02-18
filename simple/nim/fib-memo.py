'''
recursive fibonacci
  * efficient version: avoid recomputation
  * memoize with a dictionary
'''
def fib(n, D):
  if n in D:
    return D[n]
  else:
    f = fib(n-1, D) + fib(n-1, D)
    # what happens if you remove the next line ?
    D[n] = f  
    return f

'''
initialize dictionary
'''
fib_values = {0:0, 1:1} 

'''
compute 
'''
n = 100
for j in range(n):
  print(j, fib(j, fib_values))
