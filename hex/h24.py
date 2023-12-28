# simple hex player based on sets                      rbh 2024  
#   ideas from ...
#     * Michi (by Petr Baudis)
#     * Morat (by Timo Ewalds)
#     * Miaowy (by rbh)
#     * Benzene (by 
#         Broderick Arneson, Philip Henderson, Jakub Pawlewicz,
#         Aja Huang, Yngvi Bjornsson, Michael Johanson, Morgan Kan,
#         Kenny Young, Noah Weninger, Chao Gao, rbh)
#     * hex (by Luke Schultz)
#     * hsearch (by Owen Randall)

from copy import deepcopy
from random import shuffle, choice
import math
from hexio import Cell, IO

class B: ################ the board #######################

  # 2x3 board        row col       positions
  #    ...      0 0  0 1  0 2     0  1  2
  #     ...      1 0  1 1  1 2     3  4  5
  
  def __init__(self,rows,cols):
    B.r  = rows  
    B.c  = cols
    B.n  = rows*cols   # number of cells

    B.nbr_offset = (-B.n, -B.n+1, 1, B.n, B.n-1, -1)
    #   0 1
    #  5 . 2
    #   4 3

    B.border = (-4,-3,-2,-1) # top, bottom, left, right

    # parent: for union find   is_root(x): return parent[x] == x

def disp_parent(parent):  # convert parent to string picture
  psn, s = 0, ''
  for fr in range(B.h):
    s += fr*' ' + ' '.join([
    #      ('{:3d}'.format(parent[psn+k]))     \
           ('  *' if parent[psn+k]==psn+k else \
            '{:3d}'.format(parent[psn+k]))     \
           for k in range(B.w)]) + '\n'
    psn += B.w
  return s

def show_parent(P):
  print(disp_parent(P))

