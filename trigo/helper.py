"""
  * trigo helper (based on go_helper) rbh 2024
"""

"""
input, output
"""

def menu():
  m =  '\n  ' + BLACK + ' 2         play BLACK cell 2'
  m += '\n  ' + WHITE + ' 0         play WHITE cell 0'
  m += '\n  ' + EMPTY + ' 1         erase stone at cell 1'
  m += '\n   u                undo'
  return m + '\n[return]            quit\n'

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

class Game_state: 
  def __init__(self, r, c):
    self.brd = empty_board(r, c)         # empty guarded board
    self.history = [self.brd]            # history of board positions
    self.next_to_move = BLACK

  def export_gdg(self):
     print('todo')

  def status_report(self):
    self.showboard()
    print(self.score_msg())

  def requestmove(self, cmd):
    move_is_ok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = cmd[0][0]
      if color in {BLACK, WHITE, EMPTY}:
        q = cmd[1][0]
        if q.isdigit():
          if q<0 or q >= 3:
            print('\n  sorry, cells 0, 1, 2 only')
            return move_is_ok
          else:
            where = q
            if color == EMPTY: # erase move
              point_color = self.brd[where]
              if point_color == EMPTY:
                print('\n  that location is already empty')
                return move_is_ok
              else:
                self.brd = change_string(self.brd, where, EMPTY) 
                return True
            if self.brd[where] != EMPTY:
              print('\n  sorry, position occupied')
              return move_is_ok
            else:
              print('\n ok we should do something')
              if move_is_ok:
              return move_is_ok

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

def BW_to_PT(c):
  return IO_CHR[' BW'.index(c)]

def color_where(x, C):
  if x[2] == ']':
    return (EMPTY, 0) # pass move
  else:
    return (BW_to_PT(x[0]))

  p = Game_state(4, 4)
  p.interact()
