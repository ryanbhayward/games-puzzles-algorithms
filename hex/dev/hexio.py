# warning: this is not the hexio.py that unfortunately was deleted a while ago
# todo: get onto git and see if we can recover this

class Cell: #############  cells #########################
  e,b,w,ch = 0,1,2, '.*@'       # empty, black, white

  def get_ptm(ch):
    return ord(ch) >> 5 # divide by the floor of 32 get player 1 or 2 based on char * or @

  def opponent(c):
    return 3-c
