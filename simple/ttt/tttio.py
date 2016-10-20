# input-output

Cell_chars = '.xo'  # empty x o
escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (textcolor,\
               escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor)

def cell_to_char(n): return Cell_chars[n]

def char_to_cell(c): return Cell_chars.index(c)

def genmoverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid genmove request\n')
  if len(cmd)==2:
    x = Cell_chars.find(cmd[1][0])
    if x == 1 or x == 2:
      return True, cmd[1][0], ''
  return invalid

def printmenu():
  print('  x b2         play X b 2')
  print('  o e3         play O e 3')
  print('  . a2         erase a 2')
  print('  g x/o           genmove')
  print('  [return]           quit')

def showboard(psn):
  def paint(s):  # s   a string
    if len(s)>1 and s[0]==' ': 
     return ' ' + paint(s[1:])
    x = Cell_chars.find(s[0])
    if x > 0:
      return stonecolors[x] + s + colorend
    elif s.isalnum():
      return textcolor + s + colorend
    return s

  pretty = '\n   ' 
  for c in range(psn.c): 
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(psn.brd.shape[0]):
    pretty += ' ' + paint(str(1+j)) + ' '
    for k in range(psn.brd.shape[1]):
      pretty += ' ' + paint(cell_to_char(psn.brd[j][k]))
    pretty += '\n'
  print(pretty)
  print('hash ',psn.hash())
