# simplified version of nimnega_v2.py rbh 2025
def get_piles():
   while True:
       raw = input('nim game pile sizes (eg. 3 5 7)   ')
       try:
          dim = tuple( int(x) for x in raw.split() )
          if len(dim) > 0 and all(d >= 0 for d in dim): return dim
       except ValueError: pass
       print('invalid, try again')

def win_loss(istrue): return 'win' if istrue else 'loss' 
def offset(k): return ' '*(2*k+1)

"""
sd         dictionary(state: boolean), true if player-to-move wins
"""
def winning(nim_psn, sd, depth): #tuple, dictionary, recursion depth
  if nim_psn in sd:
    print(offset(depth), win_loss(sd[nim_psn]), nim_psn, 'dict')
    return sd[nim_psn]
  print(offset(depth), nim_psn)
  psn = tuple(sorted(nim_psn))
  for j in range(len(psn)): # each pile
    for k in range(psn[j]): # number stones that will remain in pile
      child = tuple(sorted(psn[:j] + (k,) + psn[j+1:]))
      if not winning(child, sd, depth+1):
        print(offset(depth), win_loss(True), nim_psn, 'losing child')
        sd.update({ nim_psn: True })   # update before return
        if depth == 0: print(len(sd), 'states')
        return True
  print(offset(depth), win_loss(False), nim_psn, 'no winning child')
  sd.update({ nim_psn: False })  # update before return
  if depth == 0: print(len(sd), 'states')
  return False

v = get_piles()
S = dict()
empty = tuple([0]*len(v))# position (0 0 ... )
S.update({empty: False}) # position (0 0 ... ) loses
w = winning(v, S, 0) 
