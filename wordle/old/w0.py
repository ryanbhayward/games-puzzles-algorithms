#!/usr/bin/env python3
"""
wordle helper rbh 2022
initial version, unfinished, awkward 
"""

from sys import stdin

SIZE = 5 # wordle length

"""
used to extract all 5-letter words from input dictionary
"""

def print5(line): # extract alphabetic, print if has 5 letters
  word = ''.join(ch for ch in line if str.isalpha(ch)) 
  if len(word) == SIZE:
    print(word.lower())

"""
the character pattern and string of forbidden characters
will be tested against each word in our dictionary
"""

def wordle_match(word, pattern, forbid):
  for j in range(SIZE):
    if (word[j] in forbid) or \
      (pattern[j].isalpha() and pattern[j] != word[j]):
      return False
  return True

"""
here is how we use the yellow wordle characters:
in each pattern so far, put character pj at some location other than j
"""

def expand(patterns, j, pj):
  new_list = []
  for X in patterns:
    print(X, j, pj)
    for k in range(5):
      if k !=j and not X[k].isalpha():
        new_string = X[:k] + pj + X[k+1:]
        new_list.append(new_string)
  return new_list

"""
using green and yellow wordle clues,
created solution-matching patterns
"""

def make_pattern(green, yellow):
  print('green  ', green, '\nyellow ', yellow)
  start = green
  assert(len(start)==5 and len(yellow)==5)
  for j in range(5):
    if str.isalpha(start[j]) and str.isalpha(yellow[j]):
      assert(False)
  print(start)
  patterns = [start]
  for p in patterns:
    for j in range(5):
      pj = yellow[j]
      if str.isalpha(pj):
        patterns = expand(patterns, j, pj)
  return patterns

green  = '.....'
yellow = '..ou.'
grey   = 'ideascrp'
patterns = make_pattern(green, yellow)
for word in stdin:
  word = word.strip()
  for p in patterns:
    if wordle_match(word, p, grey):
      print(word)
