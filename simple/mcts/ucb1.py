# implement ucb1 formula
import math

def win_rate(w,v):
  return (w + 5.0) / (v + 10.0)

def ucb(c,w,v,V):
  return win_rate(w,v) + c* math.sqrt(math.log(V)/v)

def win_rate_test(n):
  for k in range(1,n):
    for j in range(k+1):
      print(j,k, win_rate(j,k))
    print('')

def ucb_demo(n):
  c, v = .1, 1
  print('constant c', c)
  print('w v V ratios  0 1 2  .4 1 2  10 20 40  50 100 200') 
  for k in range(n):
    print('v', '{:3d}'.format(v), ' ', end='')
    print(' ', 
      '{0:.3f}'.format(ucb(c,0,v,v+v)).lstrip('0'), 
      '{:.3f}'.format(ucb(c,.4*v,v,v+v)).lstrip('0'), 
      '{:.3f}'.format(ucb(c,10*v, 20*v, 40*v)).lstrip('0'), 
      '{:.3f}'.format(ucb(c,50*v, 100*v, 200*v)).lstrip('0'))
    v *= 2

win_rate_test(8)
ucb_demo(10)
