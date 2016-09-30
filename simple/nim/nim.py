# play nim RBH 2016
# under construction
from sys import stdin

def showboard(L):
  if gameover(L): 
    return
  print('\n  ',end='')
  for j in range(len(L)):
    if L[j] > 0: print('*'*L[j], end='  ')
  print('\n  ',end='')
  for j in range(len(L)):
    if L[j] > 0: print(chr(j+ord('a')), L[j], end='   ')
  print('\n')

def gameover(L):
  for j in L:
    if j>0: return False
  return True

def makemove(c,n,L):
  pile = ord(c)-ord('a')
  if pile<0 or pile >= len(L):
    print('invalid pile')
  elif n<1 or n>L[pile]:
    print('\n   cannot take that many from pile',c)
  else:
    #print('\n ',n,'from pile',c)
    L[pile] -= n
  showboard(L)

def playgame():
  L = [3,5,7]
  showboard(L)
  while True:
    if gameover(L):
      print('\ngame over!  player who just moved wins ...\n')
      return
    cmd = input('')
    if len(cmd)==0 or cmd[0]=='q':
      print('\n ... adios :)\n')
      return
    elif cmd[0][0]=='h':
      print('a 2     remove 2 stones from pile a')
      print('?       generate computer move')
      print('h       help')
      print('q       quit')
      showboard(L)
    else: 
      cmd = cmd.split()
      if len(cmd)<2 or not cmd[1].isdigit():
        print('  move format: a 1\n')
      else:
        makemove(cmd[0][0], int(cmd[1]), L)

#L = [3,5,7]
#showboard(L)
#makemove('b',1,L)
playgame()
