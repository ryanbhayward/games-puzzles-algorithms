# input-output

Cell_chars = '*@-.'  # b w bw e 
escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor,\
               textcolor)

def cell_to_char(n):
  return Cell_chars[n]

def char_to_cell(c):
  return Cell_chars.index(c)

def genmoverequest(cmd):
    cmd = cmd.split()
    if len(cmd)==2 and cmd[1].isalpha():
      x = Cell_chars.find(cmd[1][0])
      if x == 0 or x == 1:
        return True, cmd[1][0], ''
    else:
      return False, None, '\n invalid genmove request\n'

def boardsizerequest(cmd):
  cmd = cmd.split()
  if len(cmd)==3 and cmd[1].isdigit() and cmd[2].isdigit():
    x, y = int(cmd[1]), int(cmd[2])
    if x>0 and y>0 and x<20 and y<20:
      return True,x,y,''
  return False, None, None, '\n invalid boardsize request\n'

def printmenu():
  print('\n  u          undo last move')
  print('  z x y      boardsize x y')
  print('  * b8       play * b 8')
  print('  o e11      play o e 11')
  print('  g b/w      genmove')
  print('  [return]          quit')

def showboard(hexpsn):
  def paint(s):  # s   a string
    if len(s)>1 and s[0]==' ': 
     return ' ' + paint(s[1:])
    x = Cell_chars.find(s[0])
    if x >= 0:
      return stonecolors[x] + s + colorend
    elif s.isalnum():
      return textcolor + s + colorend
    return s

  rowlabelfield = '  '
  pretty = '\n' + rowlabelfield
  pretty += '  ' * (hexpsn.rings-1) + ' '
  for c in range(hexpsn.c): 
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(hexpsn.brd.shape[0]):
    pretty += j*' '
    if j < hexpsn.rings or j >= hexpsn.rings + hexpsn.r:
      pretty += rowlabelfield
    else:
      pretty += paint('{:2}'.format(j+1-hexpsn.rings))
    for k in range(hexpsn.brd.shape[1]):
      pretty += ' ' + paint(cell_to_char(hexpsn.brd[j][k]))
    pretty += '\n'
  print(pretty)
