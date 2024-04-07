"""
game of go on a triangular 3-point board  rbh 2024
"""

from trigo_utils import Cell, Color, IO, Board
from time import time

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

class Game_state: 
  def __init__(self):
    self.board = Board.empty()
    bcopy = self.board[:]          # copy of initial board
    self.board_history  = [bcopy]  # history of boards
    self.move_history = [-1]     # history of moves
    self.next_to_move = Cell.b   # black moves first
    self.move_num = 0
    self.show_history()

  def show_history(self):
    nb = len(self.board_history)
    nm = len(self.move_history)
    assert(nb == nm)
    assert(nb == 1 + self.move_num)
    print(' history\n move cell board')
    for j in range(nb):
       print('{:4} {:4d}   {:3}'.format(j, self.move_history[j], self.board_history[j]))

  def requestmove(self, cmd):
    move_is_ok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color == 'b': color = Cell.b
      if color == 'w': color = Cell.w
      if color in Cell.io_ch:
        q = cmd[1][0]
        if q == 'p':
          print('\n    ', color, ' pass move')
        if q.isdigit():
          q = int(q)
          if q >= 3:
            print('\n  sorry, cells 0, 1, 2 only')
            return move_is_ok
          else:
            where = q
            if color == Cell.e: # erase move
              point_color = self.board[where]
              if point_color == Cell.e:
                print('\n  that location is already empty')
                return move_is_ok
              else:
                # TODO self.make_move()
                self.board = Board.change_cell(self.board, color, where) 
                return True
            if self.board[where] != Cell.e:
              print('\n  sorry, position occupied')
              return move_is_ok
            else:
              self.board = Board.change_cell(self.board, color, where) 
              return True

  def interact(self):
    gs = self
    print(IO.welcome)
    print(IO.menu)
    while True:
      Board.report(gs.board)
      cmd = input('  ')
      if len(cmd)==0:
        print('\n ... adios :)\n')
        return
      c0 = cmd[0][0]
      if c0 == 'h':
        print(IO.menu)
      elif c0 == 'u':
        gs.undo_last_action()
        if len(gs.history) > 1: 
          gs.history.pop()
      elif c0 in Cell.io_ch + 'bw':
        sofar = gs.requestmove(cmd)
      else:
        print('\n ???????\n')
        print(IO.menu)

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
Board.test(s.board)
s.interact()

