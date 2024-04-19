"""
game of go on 4-cell board  rbh 2024
"""
DSHOW = 1
MAX_SCORE = 4 # only possible scores -4, -1, 0, 1, 4
calls, max_depth, best_move = 999, 999, ''

from q_utils import Cell, Color, IO, Board, Move
from time import time
from os import system

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

class Game_state: 
  def __init__(self):
    self.board = Board.empty()
    bcopy = self.board[:]          # copy of initial board
    self.board_history  = [bcopy]  # history of boards
    self.move_history = [Move.nil] # history of moves
    self.moves_made = 0
    self.ptm = Cell.b
  
  def show_moves(self):
    s = ''
    for m in self.move_history:
      if m == Move.nil: s+= '-'
      elif m == Move.p: s+= 'p'
      else: s+= str(m)
    print(s)

  def show_moves_fancy(self):
    s, j, player = '', 0, 'BW'
    for m in self.move_history:
      if m == Move.nil: pass
      elif m == Move.p: 
        s+= str(j)+'.'+player[(j+1)%2]+'[pass] '
      else: 
        s+= str(j)+'.'+player[(j+1)%2]+'['+str(m)+'] '
      j += 1
    print(s)

  def show_history(self):
    nb = len(self.board_history)
    nm = len(self.move_history)
    assert(nb == nm)
    assert(nb == 1 + self.moves_made)
    print(Color.grn('\n history'),
          Color.mgn(' move cell board'))
    for j in range(nb):
       print(8*' ', '{:4} {:4}   {:3}'.format(j, 
         self.move_history[j], self.board_history[j]))

  def show_kids(self):
    brd = self.board
    for c in (Cell.b, Cell.w):
       print(c, 'kids')
       for k in Board.children(brd,c):
         print('     ', k)

  def make_move(self, new_psn, where):
    self.board = new_psn
    self.board_history.append(new_psn)
    self.move_history.append(where)
    self.moves_made += 1
    self.ptm = Cell.opponent(self.ptm)

  def try_move(self, new_psn, where):
    if where != Move.p and new_psn in self.board_history:
      self.fail_msg('superko violation')
      return
    self.make_move(new_psn, where)

  def undo_move(self):
    if self.moves_made == 0:
      self.fail_msg('nothing to undo')
      return
    self.board_history.pop()
    self.board = self.board_history[-1]
    self.move_history.pop()
    self.moves_made -= 1
    self.ptm = Cell.opponent(self.ptm)

  def fail_msg(self, msg):
    print(Color.mgn('\n sorry,'), end=' ')
    print(msg)

  def wrong_player_msg(self, parity):
    print(Color.mgn('\n sorry,'), end=' ')
    print('not', ("black's","white's")[1-parity], 'turn')

  def request_move(self, cmd):
    cmd = cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color == 'b': color = Cell.b
      if color == 'w': color = Cell.w
      if color == Cell.e:
        self.fail_msg('color must be black or white')
        return
      parity = self.moves_made % 2
      whose_turn = (Cell.b, Cell.w)[parity]
      if color != whose_turn:
        self.wrong_player_msg(parity)
        return
      if color in Cell.io_ch:
        q = cmd[1][0]
        if q == 'p':
          same_psn = self.board[:] # new copy
          self.try_move(same_psn, Move.p)
        if q.isdigit():
          q = int(q)
          if q >= Cell.n:
            self.fail_msg('cells 0 to '+str(Cell.n-1)+' only')
            return 
          else:
            where = q
            if self.board[where] != Cell.e:
              self.fail_msg('cell occupied')
              return 
            else:
              ok, new_psn = Board.can_play(self.board, where, color) 
              if not ok:
                self.fail_msg('self-capture not allowed')
                return
              self.try_move(new_psn, where)
              return 

  def interact(self):
    gs = self
    print(IO.welcome)
    print(IO.menu)
    while True:
      Board.report(gs.board)
      gs.show_history()
      #gs.show_kids()
      if gs.move_history[-1] == Move.p and \
         gs.move_history[-2] == Move.p:
        print('\n consecutive passes: game over ... adios :)\n')
        return
      cmd = input('  ')
      if len(cmd)==0:
        print('\n ... adios :)\n')
        return
      c0 = cmd[0][0]
      if c0 == 'h':
        print(IO.menu)
      elif c0 == 'u':
        gs.undo_move()
      elif c0 in Cell.io_ch + 'bw':
        gs.request_move(cmd)
      elif c0 == 's':
        global calls, max_depth, best_move
        calls, max_depth, best_move = 0, 0, 'none'
        s = gs.negamax(0)
        print('\n', Cell.name(gs.ptm), '-to-move, ', sep='', end='')
        print('mmx', s, 'calls', calls)
        print(' max_depth', max_depth, ' a best move', best_move)
      else:
        gs.fail_msg('could not parse request: please try again\n')
        print(IO.menu)

  def ptm_score(self):
    return Board.score(self.board) if self.ptm == Cell.b \
      else -Board.score(self.board)

  def negamax(self, d): 
    global calls, max_depth, best_move
    calls += 1
    if d > max_depth: 
      self.show_moves()
      max_depth = d
    if d <= DSHOW: 
      print('depth', d, 'psn', self.board)

    so_far = float('-inf')
    if self.move_history[-1] == Move.p: # pass move
      p_score = self.ptm_score()
    else:
      self.make_move(self.board[:], Move.p)
      p_score = -self.negamax(d+1)
      self.undo_move()
    if p_score > so_far:
      so_far = p_score
      if d==0: best_move = 'pass'
    if so_far == MAX_SCORE: return so_far

    for child in Board.children(self.board, self.ptm):
      if child[1] not in self.board_history:
        self.make_move(child[1], child[0])
        child_score = -self.negamax(d+1)
        if child_score > so_far:
          so_far = child_score
          if d==0: best_move = child[1]
        self.undo_move()
        if so_far == MAX_SCORE: return so_far

    return so_far

#start_time = time()
#print('\ntime ', time() - start_time)
#Cell.test()
system('clear')
s = Game_state()
#Board.test(s.board)
s.interact()

