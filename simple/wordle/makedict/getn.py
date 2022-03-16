#!/usr/bin/env python3
"""
reduce wordlist to n-letter-words-only wordlist
"""

from sys import stdin

SIZE = 4 # wordle length
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

for line in stdin:
  word = line.strip()
  if len(word) == SIZE and str.isalpha(word):
    print(word.lower())
