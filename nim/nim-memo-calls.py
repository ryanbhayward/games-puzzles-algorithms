# compute nim values using negamax and a dictionary
#   that holds values already computed     RBH 2019
#   2022: also show total number of recursive calls, dictionary size

def get_piles():
   while True:
       raw = input('nim game pile sizes (eg. 3 5 7)   ')
       try:
          dim = tuple( int(x) for x in raw.split() )
          if len(dim) > 0 and all(d >= 0 for d in dim):
             return dim
       except ValueError:
          pass
       print('invalid, try again')

"""
sd         dictionary(state: boolean), true if player-to-move wins
"""
def winning(nim_psn, sd, depth):  # tuple, dictionary, recursion depth
  print('  '*depth, nim_psn)
  calls = 1
  if nim_psn in sd:
    return sd[nim_psn], calls
  # nim_psn not in dictionary, so update before we return
  if all(p == 0 for p in nim_psn): # we lose if every pile empty
    sd.update({ nim_psn: False })  # update before return
    print('  '*depth, nim_psn, 'lose')
    return False, calls
  #psn = tuple(sorted(nim_psn, reverse=True))
  psn = tuple(sorted(nim_psn))
  for j in range(len(psn)): # each pile
    if j == 0 or psn[j] > psn[j-1]:
      for k in range(psn[j]): # number of stones that will remain in that pile
        child = tuple(sorted(psn[:j] + (k,) + psn[j+1:]))
        result = winning(child, sd, depth+1)
        calls += result[1]
        if not result[0]:
          sd.update({ nim_psn: True })   # update before return
          print('  '*depth, nim_psn, 'win')
          if depth == 0: 
            print('\nwinning move to ',child, ' ', calls, 'calls')    # show a winning move
          return True, calls
  sd.update({ nim_psn: False })  # update before return
  print('  '*depth, nim_psn, 'lose')
  if depth == 0: 
    print('\nlosing,', calls, 'calls')
  return False, calls

v = get_piles()
S = dict()
w = winning(v,S,0)
print('dictionary size', len(S))
