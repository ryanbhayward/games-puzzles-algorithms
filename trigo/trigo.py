"""
  * simple set-based go environment    rbh 2024
  * similar to hex.py
  * they both use hexgo.py, stone_board.py
"""

from trigo_utils import Cell, Color, IO, Board
from time import time

def menu():
  m =  '\n  cells         0 '
  m += '\n               1 2\n'
  m += '\n  x 2         play black cell 2'
  m += '\n  o 1         play white cell 1'
  m += '\n  . 0         erase stone at cell 0'
  m += '\n   u          undo'
  return m + '\n[return]      quit\n'

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

class Game_state: 

  def __init__(self):
    self.bn = Board()
    self.history = [self.bn.board]            # history of board positions
    self.next_to_move = Cell.b

  def requestmove(self, cmd):
    move_is_ok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color in Cell.io_ch:
        q = cmd[1][0]
        if q.isdigit():
          q = int(q)
          if q >= 3:
            print('\n  sorry, cells 0, 1, 2 only')
            return move_is_ok
          else:
            where = q
            if color == Cell.e: # erase move
              point_color = self.bn.board[where]
              if point_color == Cell.e:
                print('\n  that location is already empty')
                return move_is_ok
              else:
                self.bn.change_cell(color, where) 
                return True
            if self.bn.board[where] != Cell.e:
              print('\n  sorry, position occupied')
              return move_is_ok
            else:
              self.bn.change_cell(color, where) 
              return True

  def interact(self):
    p = self
    while True:
      p.bn.report()
      cmd = input('')
      if len(cmd)==0:
        print('\n ... adios :)\n')
        return
      if cmd[0][0] == 'h':
        print(menu())
      elif cmd[0][0] == 'u':
        p.undo_last_action()
        if len(p.history) > 1: 
          p.history.pop()
      elif (cmd[0][0] in Cell.io_ch):
        sofar = p.requestmove(cmd)
        #if sofar: # no liberty violation, check superko
        #  new_position = p.brd
        #  if new_position in p.history:
        #    print('superko violation, move not allowed')
        #    p.undo_last_action()
        #  else:
        #    p.history.append(new_position)
      else:
        print('\n ???????\n')
        print(menu())

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
#s.bn.report()
#s.bn.test()
s.interact()

