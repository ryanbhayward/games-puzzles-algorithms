# simple program to illustrate recursive random walk
from collections import deque
from random import shuffle
from time import sleep
from sys import stdin

# we represent a maze as a list of strings, one for each row
# you can think of this as a 2-dimensional Cartesian map,
#   where each cell is either wall, empty, origin, or destination
# we will use an extra character to mark the current cell
#   as we wander randomly thru the maze, seeking the destination
wall_ch =    'X'    # wall
origin_ch =  '+'    # origin
dest_ch =    '!'    # destination
empty_ch =   ' '   # empty cell
current_ch = '?' # current cell 
seen_ch =    '.'    # seen cell
# here are the Cartesian shifts that give us a cell's neighbours
#   1st position is row index, 2nd psn is column index
nbr_offsets = [(0,-1), (0,1), (-1,0), (1,0)] # Left Right Up Down
#nbr_offsets = [(0,-1), (-1,0), (0,1), (1,0)] # L U R D
#nbr_offsets = [(0,-1), (-1,0), (1,0), (0,1)] # L U D R

def newstring(s,index,ch):  # replace character in string
  return s[0:index]+ch+s[index+1:]

class Maze:
  """a simple maze class"""

  def __init__(self):
    self.lines = []
    for line in stdin:
      self.lines.append(line.strip('\n'))
    self.rows, self.cols = len(self.lines), len(self.lines[0])
    for j in range(1,self.rows-1):
      assert (self.cols == len(self.lines[j])) # each maze line has same len
      for line in self.lines:
        assert((line[0]==wall_ch and (line[self.cols-1]==wall_ch)))
        # top and bottom of maze must be solid wall
      for j in self.lines[0]: assert(j == wall_ch) # left wall must be solid
      for j in self.lines[self.rows-1]: assert(j == wall_ch) # rt wall must be solid

  def showpretty(self):
    for line in self.lines:
      for x in line:
        print(x,' ',end='') # add spaces for readability
      print('')
    print('')
    sleep(1.0)

  def find_start(self):
    for r in range(self.rows):
      for c in range(self.cols):
        if self.lines[r][c]==origin_ch: return r,c
    assert(False) # did not find origin_ch

  def char_at(self,psn): # the character at this position
    # psn[0] is the row index   psn[1] is the column index
    s = self.lines[psn[0]]
    return s[psn[1]]

  def mark_location(self,psn,ch): # used to show we have processed the cell
    self.lines[psn[0]] = newstring(self.lines[psn[0]],psn[1],ch)

  def rwander(self,psn): # recursive wander
    here_ch = self.char_at(psn)
    assert(here_ch == empty_ch or here_ch == origin_ch)
    if here_ch == empty_ch:
      self.mark_location(psn, current_ch)
      self.showpretty() # print maze, so we can watch the traversal
      self.mark_location(psn, seen_ch)
    for shift in nbr_offsets:
      # to move from a grid-point to a neighboring grid-point,
      #    add the associated shift value to the row and column values
      #    e.g. adding shift (0, -1) to point (3, 4) moves to point (3,3)   
      new_psn = psn[0]+shift[0], psn[1]+shift[1]
      new_ch = self.char_at(new_psn) # examine new_psn
      if new_ch == dest_ch:
        self.showpretty() # print maze, so we can watch the traversal
        return new_psn
      if new_ch == empty_ch:
        rec = self.rwander(new_psn)    # recursively traverse from new_psn
        if rec is not None:            # did recursive call find exit?
          return rec                   # yes? rwander(self,psn) terminates

  def iwander(self,psn): # iterative wander
    num_iterations = 0
    while True:
      num_iterations += 1
      if self.char_at(psn) == empty_ch:
        self.mark_location(psn,current_ch)
      self.showpretty()
      shuffle(nbr_offsets) # if you don't shuffle you might get stuck
      for shift in nbr_offsets:
        new_psn = psn[0]+shift[0],psn[1]+shift[1]
        new_ch = self.char_at(new_psn)
        if new_ch == dest_ch:
          print(num_iterations,'looks')
          return new_psn
        elif (new_ch != wall_ch):
          if self.char_at(psn) == current_ch:
            self.mark_location(psn,empty_ch)
          psn = new_psn
          break

maze = Maze() # Maze() calls __init__(maze) of class Maze
startpsn = maze.find_start() # scan the maze to find the origin location
psn = maze.rwander(startpsn) # return the value found by recursive wandering
print('finish at location',psn) # print the destination location
print('nbr_offsets',nbr_offsets) # print the destination location
