# implement ucb1 formula
import math

T = 5.0
def win_rate(w,v):
  return (w + T) / (v + T + T)

def ucb(c,w,v,V):
  return win_rate(w,v) + c* math.sqrt(math.log(V)/v)

def win_rate_test(n):
  for k in range(1,n):
    for j in range(k+1):
      print(j,k, win_rate(j,k))
    print('')

def ucb_demo(n):
  c, j = .5, 1
  print('  UCB1 formula values')
  print('win rate additive factor T', T)
  print('ucb multiplicative constant c', c)
  print('for some j, compute ucb(c, w*j, v*j, V*j)')
  print('w v V  0 1 2  1 3 6  9 20 40  100 200 400') 
  for k in range(n):
    print('j', '{:4d}'.format(j), ' ', end='')
    print( 
      '{:.3f}  '.format(ucb(c,0,  j,  2*j)).lstrip('0'), 
      '{:.3f}  '.format(ucb(c,  j,  2*j,  6*j)).lstrip('0'), 
      '{:.3f}      '.format(ucb(c,9*j, 20*j, 40*j)).lstrip('0'), 
      '{:.3f}'.format(ucb(c,100*j, 200*j, 400*j)).lstrip('0'))
    j *= 2

#win_rate_test(8)
ucb_demo(12)
