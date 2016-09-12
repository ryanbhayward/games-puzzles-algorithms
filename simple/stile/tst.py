# simple program to solve sliding tile; under construction
from random import shuffle
from time import sleep
from sys import stdin

def output_char(ch):
  if ch=='0': return('*')
  elif ord(ch) > ord('9'): 
    return(chr(7+ord(ch)))
  else: 
    return(ch)

for j in range(30):
  print(j, chr(j+ord('0')), output_char(chr(j+ord('0'))))
