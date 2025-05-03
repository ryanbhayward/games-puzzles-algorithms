#!/usr/bin/env python3
"""
wordle helper rbh 2022
- filter the word list according to the wordle guesses,
  and show the user the filtered list
"""

# TODO
#   fix helper logic: same-letter one-yellow, one-gray

import sys

SIZE = 5 # wordle length
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

"""
string stuff
"""

def delete_char(s, ch):
  return s.replace(ch,'.')

"""
using green and yellow wordle clues,
created solution-matching patterns
"""

def wordle_match(word, allowed, vacant, must_have):
  for j in range(SIZE):
    if word[j] not in allowed[j]:
      return False
  wordlet = ''
  for j in range(SIZE):
    if j in vacant:
      wordlet += word[j]
  for ch in must_have:
    if ch not in wordlet:
      return False
  return True

def wordle_prep(green, yellows, grey):
  print('\ngreen     ', green, '\nyellow(s) ', yellows[0])
  for j in range(1, len(yellows)):
    print('          ', yellows[j])
  print('grey      ', grey)

#TODO should not be hard-coded, allow for other sizes

  allowed = ['', '', '', '', '']
  for j in range(SIZE):
    allowed[j] = ALPHABET

  # process greys
  for ch in grey:
    for j in range(SIZE):
       allowed[j] = delete_char(allowed[j], ch)

  # process greens
  vacant = {0, 1, 2, 3, 4}  # indices of vacant cells
  for j in range(SIZE):
    ch = green[j]
    if str.isalpha(ch):
      vacant.remove(j)
      allowed[j] = ch

  # process yellows
  must_have = set()
  for yell in yellows:
    for j in range(SIZE):
      if str.isalpha(yell[j]):
        must_have.add(yell[j])
        allowed[j] = delete_char(allowed[j], yell[j])

  print('\nvacant', vacant, '   must_have', must_have,'\n')
  for j in range(SIZE):
    print('allowed[', j, ']', allowed[j])
  print('')

  return allowed, vacant, must_have

def get_word_list():
    word_list = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            word_list.append(line.rstrip().replace(' ', ''))
    return word_list

"""
main loop
"""

green  =   '....r'
yellows = ['.ta.e']
grey   = 'sonchidumpy'
allowed, vacant, must_have = wordle_prep(green, yellows, grey)
word_list = get_word_list()
assert(len(word_list[0])==len(green))
for word in word_list:
  if wordle_match(word, allowed, vacant, must_have):
    print(word)
