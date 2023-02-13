"""
  * go helper   (previously go_play.py)  rbh 2016-2023
      - legal moves
      - tromp taylor score
      - can take user IO, can also read from .sgf
      - export final game position as rbh .gdg format (for .eps file)
  * allow rectangular boards
             1 <= R <= 19 rows 
             1 <= C <= 19 columns
  todo * allow input illegal position, report whether position is legal
       * put more inside Game_state ?
"""

"""
board: - R rows, C columns plus guard rows/column 
       - 1-dimensional vector, row major order, bottom row first
       - string, total (R+2) * (C+1) points     
       - guards (borders) ensure each left/right/up/down point-neighbour exists,
         simplifying loop computation       e.g. empty 3x4 board:

guarded board --> g  g  g  g  g   20 21 22 23 24  <-- indices of board points
                  g  .  .  .  .   15 16 17 18 19    
                  g  .  .  .  .   10 11 12 13 14    
                  g  .  .  .  .    5  6  7  8  9          
                  g  g  g  g  g    0  1  2  3  4  <--  row-major bottom-up order     
"""

from argparse import ArgumentParser

"""
input, output
"""

IO_CHR = '.*oge'  # point characters: empty, black, white, guard
EMPTY, BLACK, WHITE, GUARD, ERASE = IO_CHR[0], IO_CHR[1], IO_CHR[2], IO_CHR[3], IO_CHR[4]
COLUMNS = 'ABCDEFGHJKLMNOPQRST'
def char_to_color(c): 
  return IO_CHR.index(c)

escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (textcolor,\
               escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor)

def paint(s):  # s   a string
  if len(s) > 1 and s[0] == ' ': 
   return ' ' + paint(s[1:])
  x = IO_CHR.find(s[0])
  if x > 0:
    return stonecolors[x] + s + colorend
  elif s.isalnum():
    return textcolor + s + colorend
  return s

def menu():
  m =  '\n  ' + BLACK + ' b2         play BLACK b 2'
  m += '\n  ' + WHITE + ' e3         play WHITE e 2'
  m += '\n  ' + EMPTY + ' d4         erase stone at d 4'
  m += '\n   u                undo'
  return m + '\n[return]            quit\n'

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

def mylabel(j):
  return '  .' if j == 0 else '{:3d}'.format(j)

class Action: # 
  def __init__(self, k, col, whr):
    self.kind, self.color, self.where = k, col, whr
  
  def show(self):
    if self.kind == Game_state.StoneCapture: msg = 'capture'
    elif self.kind == Game_state.StonePut: msg = 'put'
    elif self.kind == Game_state.Erase: msg = 'erase'
    elif self.kind == Game_state.Pass: msg = 'pass'
    msg += ' ' + self.color + str(self.where)
    return msg

class Game_state: # go board, each point in {B, W, E, G}
  StonePut, StoneCapture, Erase, Pass = 0, 1, 2, 3  #atomic helper actions
  # StonePut  put a stone on the board
  # StoneCapture  (remove a stone as part of a capturing move)
  # StoneErase   remove a stone, not part of a move, used for post-game analysis
  # Pass      pass move

  def __init__(self, r, c):
    self.R, self.C = r, c
    self.nbr_offsets = (-(c+1), -1, 1, c+1) # distance to each neighbor
    self.brd = empty_board(r, c)         # empty guarded board
    self.guarded_n = len(self.brd)       # number of points in guarded board
    self.actions = []                    # history of atomic actions
    self.history = [self.brd]            # history of board positions
    self.labels_brd = [0]*self.guarded_n # label each point with number of last move there
    self.next_to_move = BLACK

  def score_difference(self, score):
    return score[0] + score[1] - (score[2] + score[3])

  def score_msg(self): # score
    tts = self.tromp_taylor_score()
    sd = self.score_difference(tts)
    blocks = self.count_blocks()
    msg  = 'blocks (b,w) ' + str(blocks[0]) + ', ' + str(blocks[1])
    msg += '\nscore ' + str(tts) 
    if sd == 0:
      msg += ': tied'
    elif sd > 0:
      msg += ': black winning by ' + str( sd)
    else:
      msg += ': white winning by ' + str(-sd)
    return msg + '\n'

  def export_gdg(self):
    msg = self.labels_msg()
    with open('out.gdg', 'w', encoding="utf-8") as f:
      f.write(msg)

  def status_report(self):
    self.showboard()
    print(self.score_msg())

  def actions_msg(self):
    print('actions: ', end='')
    msg = ''
    for h in self.actions:
      msg += 'TCEP'[h.kind] # put capture erase pass
      msg += h.color + str(h.where) + ' '
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
      #print('removing captured group at', point_to_alphanum(where, self.C))
      for j in cap:
        self.brd = change_string(self.brd, j, EMPTY)
      return cap, True  # move ok sofar 

    if self.captured(where, color):
      print('whoops, no liberty there: not allowed')
      self.brd = change_string(self.brd, where, EMPTY) # erase the attempted move
      return cap, False  # move not possible, point occupied
    return cap, True

  def undo_last_action(self):  # undo last action
    p = self
    if len(p.actions) == 0:
      print('\n    board empty, nothing to undo\n')
    else:
      print(p.actions_msg())
      while True:
        a = p.actions.pop()
        k, c, w = a.kind, a.color, a.where
        if k == p.StoneCapture: # undo capture: restore
          p.brd = change_string(p.brd, w, c)
          # stay in loop in case more stones were captured
        elif k == p.Erase: # undo erase: restore
          p.brd = change_string(p.brd, w, c)
          return
        else: # undo stoneput: erase
          p.brd = change_string(p.brd, w, EMPTY)
          # normal move, so only one stone to erase, we are done
          print(p.actions_msg())
          return

  def requestmove(self, cmd):
    move_is_ok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color in {BLACK, WHITE, EMPTY}:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, COLUMNS.index(q.upper())
          if x<0 or x >= self.R or y<0 or y >= self.C:
            print('\n  sorry, coordinate off board')
            return move_is_ok
          else:
            where = brd_index(x, y, self.C)
            if color == EMPTY: # erase move
              point_color = self.brd[where]
              if point_color == EMPTY:
                print('\n  that location is already empty')
                return move_is_ok
              else:
                move_record = Action(self.Erase, point_color, where)
                self.actions.append(move_record) # record move for undo
                self.brd = change_string(self.brd, where, EMPTY) 
                return True
            if self.brd[where] != EMPTY:
              print('\n  sorry, position occupied')
              return move_is_ok
            else:
              move_record = Action(self.StonePut, color, where)
              captured, move_is_ok = self.makemove(where, color)
              if move_is_ok:
                self.actions.append(move_record) # record move for undo
                for x in captured: # record captured stones for undo
                  cap_action = Action(self.StoneCapture, opponent(color), x)
                  self.actions.append(cap_action)
              return move_is_ok

  def captured(self, where, color):
  # return points in captured group containing where,
  #        empty if group is not captured
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

  def count_blocks(self): 
    blocks, seen = [0, 0], set()
    for p in range(self.guarded_n):
      p_val = self.brd[p]
      if (p not in seen) and ((p_val == BLACK) or (p_val == WHITE)):
        block_points = [p]
        seen.add(p)
        blocks[IO_CHR.find(p_val)-1] += 1
        while (len(block_points) > 0):
          q = block_points.pop()
          for j in self.nbr_offsets:
            x = j + q
            if (self.brd[x] == p_val) and (x not in seen):
              block_points.append(x)
              seen.add(x)
    return blocks

  def tromp_taylor_score(self): # each player: stones, territory
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
	        
  def generate_labels(self):
    move_number, H = 0, self.actions
    for j in range(len(H)):
      act = H[j]
      #print('j', j, H[j].show())
      if (act.kind == self.StoneCapture) or (act.kind == self.Erase):
        self.labels_brd[H[j].where] = 0
      elif act.kind == self.Pass:
        move_number += 1
        ptm = self.player_to_move
        self.player_to_move = opponent(ptm)
      # later: add erase
      else:             
        move_number += 1
        self.labels_brd[H[j].where] = move_number

  def labels_msg(self):
    msg = ''
    for r in reversed(range(self.R)):
      for c in range(self.C):
        msg += mylabel(self.labels_brd[brd_index(r, c, self.C)]) + ' '
      msg += '\n'
    return msg

  def showboard(self):
    pretty = '\n    ' 
    for c in range(self.C): # columns
      pretty += ' ' + paint(COLUMNS[c])
    pretty += '\n'
    for j in reversed(range(self.R)): # rows
      pretty += ' ' + paint('{:2d}'.format(1+j)) + ' '
      for k in range(self.C): # columns
        pretty += ' ' + paint(self.brd[brd_index(j,k,self.C)])
      pretty += '\n'
    print(pretty)

  def interact(self):
    p = self
    while True:
      p.status_report()
      cmd = input('')
      if len(cmd) == 0:
        p.generate_labels()
        p.export_gdg()
        print('\n ... adios :)\n')
        return
      if cmd[0][0] == 'h':
        print(menu())
      elif cmd[0][0] == 'u':
        p.undo_last_action()
        if len(p.history) > 1: 
          p.history.pop()
      elif (cmd[0][0] in IO_CHR):
        sofar = p.requestmove(cmd)
        if sofar: # no liberty violation, check superko
          new_position = p.brd
          if new_position in p.history:
            print('superko violation, move not allowed')
            p.undo_last_action()
          else:
            p.history.append(new_position)
      else:
        print('\n ???????\n')
        print(menu())

def sgf_index(xy, C): # sgf index xy is row y (from bottom, alpha) column x
  return brd_index(ord(xy[1]) - ord('a'), ord(xy[0]) - ord('a'), C)

def BW_to_PT(c):
  return IO_CHR[' BW'.index(c)]

def color_where(x, C):
  if x[2] == ']':
    return (EMPTY, 0) # pass move
  else:
    return (BW_to_PT(x[0]), sgf_index(x[2:4], C))

def parse_token(t): # return whether-move-is-valid and move
  if len(t) < 2:
    return False, ''
  if (t[0] == 'B' or t[0] == 'W') and t[1] == '[':
    if t[2] == ']': # missing location indicates pass move
      return True, t[0] + '[]  '
    else:
      assert(t[4] == ']')
      return True, t[0:5]
  return False, ''

def parse_sgf(infile, C):
  L, M, movenum = infile.readlines(), [], 1
  for k in L:
    x = k.strip().split(';')
    for y in x:
      x = parse_token(y)
      if x[0]:
        (col, whr) = color_where(x[1], C)
        M.append([movenum, col, whr])
        movenum += 1
  return M

if __name__ == "__main__":
  parser = ArgumentParser(description='go game: user interact and/or read sgf')
  parser.add_argument('-f', '--myfile', type=open, help='name of input sgf file')
  args = parser.parse_args()
  if args.myfile:
    M = parse_sgf(args.myfile, 19)
    #for mv in M:
    #  for j in mv:
    #    print(j, end=' ')
    #  print('')
    p = Game_state(19,19)
    for mv in M:
      #p.status_report()
      color, where = mv[1], mv[2]
      move_record = Action(p.StonePut, color, where)
      if color != EMPTY:  # ignore pass moves
        captured, move_is_ok = p.makemove(where, color)
        assert move_is_ok, 'invalid move from sgf game'
        for x in captured: # record captured stones for undo
          cap_action = Action(p.StoneCapture, opponent(color), x)
          #print('reached sgf capture', cap_action.show())
          p.actions.append(cap_action)
        new_position = p.brd
        assert new_position not in p.history, 'sgf input: superko violation'
      p.actions.append(move_record) # record move for undo
    p.showboard()
  else:
    p = Game_state(4, 4)
  p.interact()
