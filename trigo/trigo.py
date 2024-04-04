"""
  * simple set-based go environment    rbh 2024
  * similar to hex.py
  * they both use hexgo.py, stone_board.py
"""

from trigo_utils import Cell, Color, IO, Pt, Board
from time import time

start_time = time()
IO.test()
print('\ntime ', time() - start_time)
