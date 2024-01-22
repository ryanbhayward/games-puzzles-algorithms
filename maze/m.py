# simple program to illustrate bfs, dfs maze traversal  (RBH+Noah 2016)
from collections import deque # double-ended queue, can pop from either end
from random import shuffle
from time import sleep
from sys import stdin

wall_ch = 'X'  # maze wall
empt_ch = ' '  # maze empty space, not yet seen
orgn_ch = '+'  # traversal origin
dest_ch = '!'  # traversal destination
seen_ch = '.'  # cell has been seen and is in queue
done_ch = '~'  # cell has been removed from queue, processing complete
nbr_offsets = [(0,-1), (0,1), (-1,0), (1,0)]

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
      for j in self.lines[0]: assert(j == wall_ch) # left wall not solid
      for j in self.lines[self.rows-1]: assert(j == wall_ch) # rt wall not solid

  def showpretty(self):      
    for line in self.lines:
      for x in line:
        print(x,' ',end='') # add spaces for readability
      print('')
    print('') 
    sleep(.3)

  def find_start(self):
    for r in range(self.rows):
      for c in range(self.cols):
        if self.lines[r][c]==orgn_ch: return r,c
    assert(False) # did not find orgn_ch

  def char_at(self,psn): # the character at this position
    s = self.lines[psn[0]]
    return s[psn[1]]

  def mark_location(self,psn,ch): # used to show we have processed the cell
    self.lines[psn[0]] = newstring(self.lines[psn[0]],psn[1],ch)

  def wander(self, count):  # using deque, yields bfs or dfs ... woo hoo :)
    psn = self.find_start()
    fringe = deque()  # the empty cells we encounter
    fringe.append(psn)
    while len(fringe) > 0:
      # comment out one of these two lines
      psn = fringe.pop() # pop from end of list, LIFO, stack
      #psn = fringe.popleft() # pop from front, FIFO, queue, so BFS
      shuffle(nbr_offsets) # just for fun
      for shift in nbr_offsets: # do you see how this works ?
        new_psn = psn[0]+shift[0], psn[1]+shift[1]
        new_ch = self.char_at(new_psn)
        if new_ch == dest_ch: return new_psn
        elif new_ch == empt_ch: 
          fringe.append(new_psn)  # append to end of list
          if count < 10:
            self.mark_location(new_psn, '0123456789'[count])
            count += 1
          else:
            self.mark_location(new_psn, seen_ch)
          self.showpretty()

maze = Maze()
maze.showpretty()
startpsn = maze.find_start()
psn = maze.wander(0)
print('finish at location',psn)
