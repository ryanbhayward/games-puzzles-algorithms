# hex player, based in part on Michi by Petr Baudis RBH 2016
import numpy as np

### cells ###############

class Cell: # each cell: empty, b, w  (bw for off-board corners)
  e,b,w,bw, ch = 0,1,2,3, '.*@-' 

def opponent(c): 
  return 3-c

### board dimensions #####

R, C  = 6, 6    # rows, columns
N     = R*C      # number of cells
W     = C + 2    # add 1 row/col per border, W is width of padded board

#   -*******-
#    o......o
#     o......o
#      o......o
#       o......o
#        o......o
#         o......o
#          -******-

### empty padded board

empty = '\n'.join(['-' + C * '*' + '-'] + 
              R * ['@' + C * '.' + '@'] +
                  ['-' + C * '*' + '-'])

letters = 'abcdefghijklmnopqrstuvwxyz'


### user i-o

# for colored output
esc       = '\033['
endcolor  =  esc + '0m'
textcolor =  esc + '0;37m'
color_of  = (textcolor, esc + '0;35m', esc + '0;32m', textcolor)

def paint(s):  # s   a string
  p = ''
  for c in s:
    x = Cell.ch.find(c)
    if x >= 0:
      p += color_of[x] + c + endcolor
    elif c.isalnum():
      p += textcolor + c + endcolor
    else: p += c
  return p

def display_brd(brd):
#  -***-             a b c
#  o...o            1 . . . o
#  o...o    ==>      2 . . . o
#  o...o              3 . . . o
#  -***-               - * * * -

  d = '   ' + ' '.join(letters[0:C]) + '\n'
  X = ' '.join(brd).split('\n')
  for j in range(1,R+1): 
    d += ' '*j + '{:2d}'.format(j)+ X[j][2:] + '\n'
  d += ' '*(R+1) + X[R+1] + '\n'
  return d
  
print(empty, '\n')
print(display_brd(empty))
print(paint(display_brd(empty)))
print(paint(empty), '\n')
