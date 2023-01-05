"""
modified go_play.py: this uses only one board rep'n RBH 2022
  * generate legal moves and game score
  * some ideas from M Mueller's go code
  * allow rectangular boards, so with columns != rows
             1 <= R <= 19 rows 
             1 <= C <= 19 columns
  * read game from sgf, in this case also create a moves board
      so that the final game position can be output as gdg file
      plan:
       - use -f feature to read sgf
       - read moves from sgf
       - make moves as usual and also on moves_board
       - export gdg file

TODO
    - add feature that reports whether position is legal
"""

"""
the board: a one-dimensional vector of points

to simplify loop computation, add three row of guard stones:
  * one row at top 
  * one row at bottom
  * one row at left 
so R x C board requires total (R+2) * (C+1) points:

  3x4 board      positions in string representing the board

 g  g  g  g  g   20 21 22 23 24
 g  .  .  .  .   15 16 17 18 19
 g  .  .  .  .   10 11 12 13 14
 g  .  .  .  .    5  6  7  8  9  
 g  g  g  g  g    0  1  2  3  4     <= in go, label rows from the bottom      
"""

"""
points on the board
"""

POINT_CHARS = '.*og'
EMPTY, BLACK, WHITE, GUARD = POINT_CHARS[0], POINT_CHARS[1], POINT_CHARS[2], POINT_CHARS[3]
COLUMNS = 'ABCDEFGHJKLMNOPQRST'
EMPTY_MOVE = 0

def opponent(color): 
  if color == BLACK: 
    return WHITE
  elif color == WHITE: 
    return BLACK
  else: 
    assert False, 'defined only for Black, White'

def empty_board(r, c):
  board = GUARD*(c+1)         # bottom row
  for rows in range(r):
    board += GUARD + EMPTY*c  # middle rows
  board += GUARD*(c+1)        # top row
  return board

def coord_to_point(r, c, C): 
  return (C+1) * (r+1) + c + 1

def moves_board_index(r, c, C):
  return C*r + c

def point_to_alphanum(p, C):
  r, c = divmod(p, C+1)
  return COLUMNS[c-1] + str(r+1)

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

class Position: # go board, each point in {B, W, E, G}
  def legal_moves(self):
    L = []
    for j in range(self.guarded_n):
      if self.brd[j] == EMPTY: 
        L.append(j)
    return L

  def __init__(self, r, c):
    self.R, self.C = r, c
    self.nbr_offsets = (-(c+1), -1, 1, c+1) # distance to each neighbor
    self.brd = empty_board(r, c)
    self.moves_brd = [EMPTY_MOVE]*r*c         # each occupied point has its move number
    print(self.moves_brd)
    self.guarded_n = len(self.brd)      # number of points in guarded board

  def show_moves_board(self):
    r, c = self.R, self.C
    for j in reversed(range(r)):  # show moves from bottom up in go
      for k in range(c):
        print('{:3d}'.format(self.moves_brd[moves_board_index(j,k,c)]), end = ' ')
      print('')
    
  def makemove(self, where, color):
    assert (self.brd[where] == EMPTY), 'that point is not empty'
    self.brd = change_string(self.brd, where, color) 

    cap = []
    for j in self.nbr_offsets:
      x = where + j
      if self.brd[x] == opponent(color):
        cap += self.captured(x, opponent(color))

    if (len(cap)>0):
      print('removing captured group at', point_to_alphanum(where, self.C))
      for j in cap:
        self.brd = change_string(self.brd, j, EMPTY)
      return cap, True  # move ok sofar 

    if self.captured(where, color):
      print('whoops, no liberty there: not allowed')
      self.brd = change_string(self.brd, where, EMPTY)
      return cap, False  # move not possible, point occupied
    return cap, True

  def requestmove(self, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color in {BLACK, WHITE, EMPTY}:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x<0 or x >= self.R or y<0 or y >= self.C:
            print('\n  sorry, coordinate off board')
            return parseok
          else:
            where = coord_to_point(x, y, self.C)
            if self.brd[where] != EMPTY:
              print('\n  sorry, position occupied')
              return parseok
            else:
              move_record = (color, where, False)
              print('move record', move_record)
              captured, parseok = self.makemove(where, color)
              if parseok:
                H.append(move_record) # record move for undo
                for x in captured: # record captured stones for undo
                  cap_record = (opponent(color), x, True)
                  #print('capture record', cap_record)
                  H.append(cap_record)
              return parseok

  def captured(self, where, color):
  # return points in captured group containing where
  #   empty if group is not captured
    assert (self.brd[where] == color)
    j, points, seen = 0, [where], {where}
    while (j < len(points)):
      p = points[j]
      for q in self.nbr_offsets:
        nbr = p+q
        if self.brd[nbr] == EMPTY: # group has liberty, not captured
          return []
        if (self.brd[nbr] == color) and (nbr not in seen):
          points.append(nbr)
          seen.add(nbr)
      j += 1
    # group is captured
    return points

  def tromp_taylor_score(self):
    bs, bt, ws, wt, empty_seen = 0, 0, 0, 0, set()
    for p in range(self.guarded_n):
      if   self.brd[p] == BLACK: 
        bs += 1
      elif self.brd[p] == WHITE: 
        ws += 1
      elif (self.brd[p] == EMPTY) and (p not in empty_seen):
        b_nbr, w_nbr = False, False
        empty_seen.add(p)
        empty_points = [p]
        territory = 1
        while (len(empty_points) > 0):
          q = empty_points.pop()
          for j in self.nbr_offsets:
            x = j + q
            b_nbr |= (self.brd[x] == BLACK)
            w_nbr |= (self.brd[x] == WHITE)
            if self.brd[x] == EMPTY and x not in empty_seen:
              empty_seen.add(x)
              empty_points.append(x)
              territory += 1
        if   b_nbr and not w_nbr: 
          bt += territory
        elif w_nbr and not b_nbr: 
          wt += territory
    return bs, bt, ws, wt
	        
"""
input, output
"""

def char_to_color(c): 
  return POINT_CHARS.index(c)

escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (textcolor,\
               escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor)

def printmenu():
  print('  h             help menu')
  print('  '+ BLACK +  ' b2         play BLACK b 2')
  print('  '+ WHITE +  ' e3         play WHITE e 2')
  print('  u                  undo')
  print('  [return]           quit')

def showboard(psn):
  def paint(s):  # s   a string
    if len(s) > 1 and s[0] == ' ': 
     return ' ' + paint(s[1:])
    x = POINT_CHARS.find(s[0])
    if x > 0:
      return stonecolors[x] + s + colorend
    elif s.isalnum():
      return textcolor + s + colorend
    return s

  pretty = '\n    ' 
  for c in range(psn.C): # columns
    pretty += ' ' + paint(COLUMNS[c])
  pretty += '\n'
  for j in range(psn.R-1, -1, -1): # rows
    pretty += ' ' + paint('{:2d}'.format(1+j)) + ' '
    for k in range(psn.C): # columns
      pretty += ' ' + paint(psn.brd[coord_to_point(j,k,psn.C)])
    pretty += '\n'
  print(pretty)

def undo(H, p):  # undo last move
  if len(H) == 0:
    print('\n    board empty, nothing to undo\n')
  else:
    while True:
      print(H)
      color, where, is_capture = H.pop()
      if is_capture: # capture move, restore it
        p.brd = change_string(p.brd, where, color)
        # stay in loop in case more stones were captured
      else: # normal move, erase it
        p.brd = change_string(p.brd, where, EMPTY)
        # normal move, so only one stone to erase, we are done
        return

def score_difference(score):
  return score[0] + score[1] - (score[2] + score[3])

def report(p):
  p.show_moves_board()
  with open('out.gdg', 'w', encoding="utf-8") as f:
    tts = p.tromp_taylor_score()
    sd = score_difference(tts)
    f.write('score ' + str(tts))
    if sd == 0:
      f.write(': draw\n')
    elif sd > 0:
      f.write(': black wins by ' + str(sd) + ' \n')
    else:
      f.write(': white wins by ' + str(-sd) + ' \n')

def interact(use_tt):
  p = Position(2, 3)
  move_record = []    # used for undo, only need locations
  positions = [p.brd] # used for positional superko
  move_made = False
  while True:
    showboard(p)
    report(p)
    for x in positions: print(x)
    print('move_record', move_record)
    print('tromp-taylor score (black, white)',p.tromp_taylor_score(),'\n')
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      undo(move_record, p)
      if len(positions)>1: positions.pop()
    elif (cmd[0][0] in POINT_CHARS):
      sofar = p.requestmove(cmd, move_record)
      if sofar: # no liberty violation, check superko
        pstring = p.brd
        if pstring in positions:
          print('superko violation, move not allowed')
          undo(move_record, p)
        else:
          positions.append(pstring)
    else:
      print('\n ???????\n')
      printmenu()

interact(False)
