"""
  * go helper
      - legal moves
      - tromp taylor score
      - user IO combined with reading from .sgf
  * allow rectangular boards
             1 <= R <= 19 rows 
             1 <= C <= 19 columns
  * previously go_play.py           rbh 2016 - 2023

in progress

  * allow read game from sgf (use python argparser)
      - in this case also create a moves_board
        that for each point shows last move there
  * export final game in .gdg format
       - use -f feature to read sgf
       - make moves as usual and also on moves_board

todo
  * allow input illegal position, report whether position is legal
"""

"""
board: a string, a 1-dimensional vector of points, e.g. empty 3x4 board:

 g  g  g  g  g   20 21 22 23 24    <-- this is called a guarded board rep'n
 g  .  .  .  .   15 16 17 18 19    
 g  .  .  .  .   10 11 12 13 14    <-- these are indices of the board points
 g  .  .  .  .    5  6  7  8  9          in the guarded board string
 g  g  g  g  g    0  1  2  3  4    <-- in go, label rows from bottom      

guards (borders) ensure each left/right/up/down point-neighbour exists,
  which simplifies loop computation
  * guard row at top     * guard row at bottom    * guard column at left 

board (R rows, C columns) represented by string ((R+2) * (C+1) points)
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

def brd_index(r, c, C): # index in points board of point (r, c)
  return (C+1) * (r+1) + c + 1

def point_to_alphanum(p, C):
  r, c = divmod(p, C+1)
  return COLUMNS[c-1] + str(r+1)

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

class Position: # go board, each point in {B, W, E, G}
  def __init__(self, r, c):
    self.R, self.C = r, c
    self.nbr_offsets = (-(c+1), -1, 1, c+1) # distance to each neighbor
    self.brd = empty_board(r, c)        # empty guarded board
    self.guarded_n = len(self.brd)      # number of points in guarded board
    self.moves_brd = [0]*self.guarded_n # each point: number of last move made there

  def moves_brd_msg(self, M):
    print(M)
    msg = ''
    for r in reversed(range(self.R)):
      for c in range(self.C):
        msg += '{:3d}'.format(M[brd_index(r, c, self.C)]) + ' '
      msg += '\n'
    return msg

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
      self.brd = change_string(self.brd, where, EMPTY) # erase the attempted move
      return cap, False  # move not possible, point occupied
    return cap, True

  def requestmove(self, cmd, H):
    move_is_ok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color in {BLACK, WHITE, EMPTY}:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x<0 or x >= self.R or y<0 or y >= self.C:
            print('\n  sorry, coordinate off board')
            return move_is_ok
          else:
            where = brd_index(x, y, self.C)
            if self.brd[where] != EMPTY:
              print('\n  sorry, position occupied')
              return move_is_ok
            else:
              move_record = (color, where, False)
              #print('move record', move_record)
              captured, move_is_ok = self.makemove(where, color)
              if move_is_ok:
                H.append(move_record) # record move for undo
                for x in captured: # record captured stones for undo
                  cap_record = (opponent(color), x, True)
                  #print('capture record', cap_record)
                  H.append(cap_record)
              return move_is_ok

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
      pretty += ' ' + paint(psn.brd[brd_index(j,k,psn.C)])
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

def score_msg(p): # score
  tts = p.tromp_taylor_score()
  sd = score_difference(tts)
  msg = 'score ' + str(tts) 
  if sd == 0:
    msg += ': tied\n'
  elif sd > 0:
    msg += ': black winning by ' + str( sd) + ' \n'
  else:
    msg += ': white winning by ' + str(-sd) + ' \n'
  return msg

def report(p, M):
  msg = 'moves board\n'
  msg += p.moves_brd_msg(M)
  msg += '\n' + score_msg(p)
  with open('out.gdg', 'w', encoding="utf-8") as f:
    f.write(msg)

def status_report(p, m):
  showboard(p)
  report(p, m)
  print('move_record', m)
  print(score_msg(p))

def generate_moves_board(p, H):
  moves_brd = [0]*p.guarded_n  # each point: number of last move made there
  move_number = 0
  for j in range(len(H)):
    if H[j][2]: # capture_move
      moves_brd[j] = 0
    else:
      move_number += 1
      if p.brd[H[j][1]] != EMPTY:
        moves_brd[H[j][1]] = move_number
  return moves_brd

def interact(use_tt):
  p = Position(2, 3)
  moves_list = []        # each entry is move or removal of captured stone
  game_history = [p.brd] # used for positional superko
  while True:
    status_report(p, moves_list)
    cmd = input(' ')
    if len(cmd) == 0:
      mb = generate_moves_board(p, moves_list)
      print(moves_brd_msg(p, mb))
      print('\n ... adios :)\n')
      return
    if cmd[0][0] == 'h':
      printmenu()
    elif cmd[0][0] == 'u':
      undo(moves_list, p)
      if len(game_history) > 1: 
        game_history.pop()
    elif (cmd[0][0] in POINT_CHARS):
      sofar = p.requestmove(cmd, moves_list)
      if sofar: # no liberty violation, check superko
        pstring = p.brd
        if pstring in game_history:
          print('superko violation, move not allowed')
          undo(moves_list, p)
        else:
          game_history.append(pstring)
    else:
      print('\n ???????\n')
      printmenu()

interact(False)
