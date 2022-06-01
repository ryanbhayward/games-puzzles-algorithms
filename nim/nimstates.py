# using recursion, compute the number of nodes in the nim state space
#   in three different cases        RBH 2019
# 1)  search space is a tree, no check for isomorphism,
#       e.g. six permutations of (1 2 3) are considered different
# 2)  search space is a tree, but check for isomorphism,
#       e.g. six permutations (1 2 3) are considered the same
#       ... this reduces the number of children of a node
# 3)  search space is a dag... so the number of nodes
#       in the search space is just the number of
#       positions reachable from the original ...
#       there will be no duplicate nodes because of transposition

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
use this if you want to show binary rep. of pile sizes
"""
def iterable_to_str(v):
# iterable of ints => concatentation of binary representations
  return ' '.join([bin(j)[2:] for j in v])  # [2:] ignores 0b prefix

"""
nim_psn    nim position at root of search tree
sd         dictionary of tree sizes
srt        group all position permutations into one equivalence class?
           return number of nodes in search tree
"""
def tree_size(nim_psn, sd, srt):  # tuple, dictionary, boolean
  ts = 1 # count root position
  if nim_psn in sd:
    return sd[nim_psn]
  if all(p == 0 for p in nim_psn):
    sd.update({ nim_psn: ts })
    return ts
  psn = tuple(sorted(nim_psn)) if srt else nim_psn
  children = set() # if srt, use for children
  for j in range(len(psn)):
    for k in range(psn[j]):
      new = psn[:j] + (k,) + psn[j+1:]
      if srt: children.add(tuple(sorted(new)))
      else:   ts += tree_size(new, sd, srt)
  if srt:
    for new in children:
      ts += tree_size(new, sd, srt)
  sd.update({ psn: ts })
  return ts

def dag_nodes(nim_psn,S): # return set of nodes in DAG
  S.add(nim_psn)
  if all(p == 0 for p in nim_psn):
    return S
  psn = tuple(sorted(nim_psn))
  for j in range(len(psn)):
    for k in range(psn[j]):
      new = psn[:j] + (k,) + psn[j+1:]
      new = tuple(sorted(new))
      if new not in S: 
        S = dag_nodes(new, S)
  return S

v = get_piles()
for b in [False, True]:
  TS = dict() # tree sizes
  print(tree_size(v, TS, b))
S = set()
S = dag_nodes(v, S)
print(len(S))
#for j in S:
#  print(j)
