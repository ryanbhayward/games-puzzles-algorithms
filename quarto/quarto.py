#!/usr/bin/env python3

# - represent quarto state as sequence of 16 4-bit integers
# - TODO simulate random games

#STATE = tuple(16*[-1])
STATE = tuple(range(16))

FILES = ((0,1,2,3),(4,5,6,7),(8,9,10,11),(12,13,14,15),
         (0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
         (0,5,10,15),(3,6,9,12))

def mybin(k):
  if k < 0:
    return(' -- ')
  return ('000' + bin(k)[2:])[-4:]

def show(st):
  for k in range(16):
    print(mybin(STATE[k]), end=' ')
    if (k%4) == 3:
      print()

def wins(f):
  file = FILES[f]
  for j in range(4):
    if STATE[file[j]] < 0: 
      return False
  for power in [2,4,8,16]:
    if STATE[file[0]]%power == STATE[file[1]]%power and \
       STATE[file[0]]%power == STATE[file[2]]%power and \
       STATE[file[0]]%power == STATE[file[3]]%power:
      return True
  return False

show(STATE)

for j in range(10):
  print(j, 'wins' if wins(j) else 'loses')
