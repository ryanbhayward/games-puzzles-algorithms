#     -- HSinput.py --
E,B,W = 0,1,2

def eg66(d, hex_brd):
  #6x6 centre-win pv
  assert(d == 6)
  hex_brd[20] = B
  hex_brd[15] = W

  #hex_brd[14] = W
  #hex_brd[15] = B
  #hex_brd[4] = W
  #hex_brd[5] = B
  #hex_brd[10] = W
  #hex_brd[11] = B
  #hex_brd[16] = W
  #hex_brd[17] = B
  #hex_brd[22] = W
  #hex_brd[23] = B
  #hex_brd[34] = W
  #hex_brd[28] = B

def eg44b2(d, hex_brd):
  #4x4 obtuse
  assert(d == 4)
  hex_brd[12] = B
  hex_brd[9] = W
  hex_brd[6] = B
  hex_brd[2] = B
  hex_brd[3] = B

def eg44c(d, hex_brd):
  #4x4 off-obtuse
  assert(d == 4)
  hex_brd[8] = B
  hex_brd[6] = W
  hex_brd[5] = B
  hex_brd[1] = B
  hex_brd[2] = B
  hex_brd[12] = W
  hex_brd[9] = B
  hex_brd[13] = W

def eg44b(d, hex_brd):
  #4x4 obtuse
  assert(d == 4)
  hex_brd[12] = B
  hex_brd[5] = W
  #hex_brd[6] = B

def eg44(d, hex_brd):
  #4x4 centre
  assert(d == 4)
  #hex_brd[9] = B

def eg33c(d, hex_brd):
  #3x3 near-obtuse
  assert(d == 3)
  hex_brd[3] = B
  hex_brd[6] = W
  hex_brd[5] = B
  hex_brd[4] = W

def eg33b(d, hex_brd):
  #3x3 obtuse
  assert(d == 3)
  hex_brd[6] = B
  hex_brd[1] = W

def eg33(d, hex_brd):
  #3x3 centre
  assert(d == 3)
  #hex_brd[4] = B

def eg22(d, hex_brd): 
  assert(d == 2)
  #hex_brd[1] = B
