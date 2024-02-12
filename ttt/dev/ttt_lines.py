# 2019 RBH    started lines-based ttt program
import numpy as np
# TODO
#  - switch to lines format?
#  - lines format: record impossible-to-complete lines
#  - check for winning move (any linesum 2) before search
#  - check for no-win-possible (all lines impossible-to-complete)
#  - check for forced moves (no win possible: block winning opponent moves)

# Cells
#          0  1  2    <- row 0   R0
#          3  4  5    <- row 1   R1
#          6  7  8    <- row 2   R2
#        /         \
#       /  |  |  |  \
#    D0   C0 C1 C2    D1   three columns and two diagonals

Empty, Black, White, Num_Cells, Num_Lines = -1, 0, 1, 9, 8
R0, R1, R2, C0, C1, C2, D0, D1 =    0, 1, 2, 3, 4, 5, 6, 7

Lines  = np.array([                   # each line is a list of cells
    [0, 1, 2], [3, 4, 5], [6, 7, 8],     
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]] )
Lines_Meeting = [
    np.array([R0, C0, D0]), np.array([R0, C1]        ), np.array([R0, C2, D1]),
    np.array([R1, C0]    ), np.array([R1, C1, D0, D1]), np.array([R1, C2]    ),
    np.array([R2, C0, D1]), np.array([R2, C1]        ), np.array([R2, C2, D0])]
Line_Sums = np.array(
    [[0] * Num_Cells, [0] * Num_Cells ])  # for Black, White

Board  = np.array([Empty] * Num_Cells)

def addStone(yes, B, c, color):
  if yes: # adding stone
    assert(B[c] == Empty)
    B[c] = color
    for line in Lines_Meeting[c]:
      Line_Sums[color][line] += 1
  else:  # removing stone
    assert(B[c] == color)
    B[c] = Empty
    for line in Lines_Meeting[c]:
      Line_Sums[color][line] -= 1

print(Lines)
print(Board)
print(Lines_Meeting)
print(Line_Sums)
for cell in [0, 3, 6]: addStone(True, Board, cell, Black)
print(Line_Sums)
for cell in [0, 3, 6]: addStone(False, Board, cell, Black)
print(Line_Sums)
for cell in [2, 5, 8]: addStone(True, Board, cell, Black)
print(Line_Sums)
for cell in [2, 5, 8]: addStone(False, Board, cell, Black)
print(Line_Sums)
