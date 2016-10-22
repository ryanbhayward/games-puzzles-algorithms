# hex player, based in part on Michi by Petr Baudis RBH 2016
import numpy as np

class Cell: # each cell: empty, b, w  (bw for off-board corners)
  e,b,w,bw, ch = 0,1,2,3, '.*@-' 
def opponent(c): return 3-c

R, C  = 4, 10  # rows, columns
N     = R*C      # number board cells
W     = C + 2    # add 1 row/col per border, W is width of padded board
empty = '\n'.join(['-' + C * '*' + '-'] +    # empty padded board
              R * ['@' + C * '.' + '@'] +
                  ['-' + C * '*' + '-'])
letters = 'abcdefghijklmnopqrstuvwxyz'


############################
# user i-o

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
  x, d, row = ' '.join(brd), '   ', 0
  for c in range(C):
    d += ' ' + letters[c]
  d += '\n'
  for line in x.split('\n'):
    row += 1
    if row==1:
      d += '   ' + line + '\n'
    elif row <= R + 1:
      d += (row-1)*' ' + '{:2}'.format(row-1) + line + '\n'
    else:
      d += (row-1)*' ' + '  ' + line + '\n'
  return d

print(empty, '\n')
print(display_brd(empty))
print(paint(display_brd(empty)))
print(paint(empty), '\n')
