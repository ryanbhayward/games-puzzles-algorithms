#!/usr/bin/env python3
# compute nim values using negamax and a dictionary
#   that holds values already computed     RBH 2019
# version 2.0 December 2020 new features
#  - verbose option, showing win/loss value once it is known
#  - move initialization of the start position outside the main loop
#  - tidying, e.g. pad variable instead of '  '

def get_piles():
   while True:
       raw = input('nim game pile sizes (eg. 3 5 7)   ')
       try:
          dim = tuple( int(x) for x in raw.split() )
          if len(dim) > 0 and all(d >= 0 for d in dim): return dim
       except ValueError: pass
       print('invalid, try again')

def win_loss(b): return 'win' if b else 'loss' 

"""
sd         dictionary(state: boolean), true if player-to-move wins
"""
def winning(nim_psn, sd, depth, verbose):  
# tuple, dictionary, recursion depth, verbose mode (True/False)
  pad = '  '
  if nim_psn in sd:
    if depth==0: print('solved before search')
    if verbose: print(pad*depth, nim_psn, win_loss(sd[nim_psn]), 'dict')
    return sd[nim_psn]
  # nim_psn not in dictionary, so update before we return
  if verbose: print(pad*depth, nim_psn)
  psn = tuple(sorted(nim_psn))
  for j in range(len(psn)): # each pile
    for k in range(psn[j]): # number of stones that will remain in that pile
      child = tuple(sorted(psn[:j] + (k,) + psn[j+1:]))
      if not winning(child, sd, depth+1, verbose):
        if verbose: print(pad*depth, nim_psn, win_loss(True), 'losing child')
        sd.update({ nim_psn: True })   # update before return
        if depth == 0: print('\nwin: move to ',child, len(sd), 'states') # show a winning move
        return True
  if verbose: print(pad*depth, nim_psn, win_loss(False), 'no win')
  sd.update({ nim_psn: False })  # update before return
  if depth == 0: print('\nloss,', len(sd), 'states')
  return False

v = get_piles()
S = dict()
empty = tuple([0]*len(v))# position (0 0 ... )
S.update({empty: False}) # position (0 0 ... ) loses
w = winning(v, S, 0, True) 
