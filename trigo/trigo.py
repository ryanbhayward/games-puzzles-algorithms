"""
game of go on a triangular 3-point board  rbh 2024
"""

from trigo_utils import Cell, Color, IO, Board, Move
from time import time

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

class Game_state: 
  def __init__(self):
    self.board = Board.empty()
    bcopy = self.board[:]          # copy of initial board
    self.board_history  = [bcopy]  # history of boards
    self.move_history = [Move.nil] # history of moves
    self.moves_made = 0

  def show_history(self):
    nb = len(self.board_history)
    nm = len(self.move_history)
    assert(nb == nm)
    assert(nb == 1 + self.moves_made)
    print(Color.grn(' history'),
          Color.mgn(' move cell board'))
    for j in range(nb):
       print(8*' ', '{:4} {:4}   {:3}'.format(j, 
         self.move_history[j], self.board_history[j]))

  def make_move(self, new_psn, where):
     self.board = new_psn
     self.board_history.append(new_psn)
     self.move_history.append(where)
     self.moves_made += 1

  def undo_move(self):
    if self.moves_made == 0:
      print(' nothing to undo')
      return
    self.board_history.pop()
    self.move_history.pop()
    self.moves_made -= 1

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
        print(Color.mgn('\n sorry,'), 
          'color must be black or white')
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
          self.make_move(same_psn, Move.p)
        if q.isdigit():
          q = int(q)
          if q >= 3:
            print(Color.mgn('\n  sorry,'), end=' ')
            print('cells 0, 1, 2 only')
            return 
          else:
            where = q
            if self.board[where] != Cell.e:
              print('\n  sorry, position occupied')
              return 
            else:
              new_psn = Board.change_cell(self.board, color, where) 
              self.make_move(new_psn, where)
              return 

  def request_fail(self):
    print('\n ???????\n')
    print(IO.menu)

  def interact(self):
    gs = self
    print(IO.welcome)
    print(IO.menu)
    while True:
      Board.report(gs.board)
      gs.show_history()
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
      else:
        gs.request_fail()

def BW_to_PT(c):
  return IO_CHR[' BW'.index(c)]

def color_where(x, C):
  if x[2] == ']':
    return (Cell.e, 0) # pass move
  else:
    return (BW_to_PT(x[0]))

#start_time = time()
#print('\ntime ', time() - start_time)
#Cell.test()
s = Game_state()
#Board.test(s.board)
s.interact()

