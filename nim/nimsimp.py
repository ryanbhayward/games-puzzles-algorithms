# simplified version of nimnega_v2.py rbh 2025
def piles():
   while True:
       raw = input('nim game pile sizes (eg. 3 5 7)   ')
       try:
          dim = tuple( int(x) for x in raw.split() )
          if len(dim) > 0 and all(d >= 0 for d in dim): return dim
       except ValueError: pass
       print('invalid, try again')

def wins(psn, sd, d): #sd: state dict
  if psn in sd:
    print('  '*d,psn,sd[psn],'dict')
    return sd[psn]
  print('  '*d,psn)
  psn = tuple(sorted(psn))
  for j in range(len(psn)): 
    for k in range(psn[j]): 
      child = tuple(sorted(psn[:j]+(k,)+psn[j+1:]))
      if not wins(child,sd,d+1):
        print('  '*d,psn,True,'losing child')
        sd.update({ psn: True })
        if d == 0: print(len(sd),'states')
        return True
  print('  '*d, psn, False)
  sd.update({ psn: False }) 
  if d == 0: print(len(sd), 'states')
  return False

v = piles();S=dict();e=tuple([0]*len(v))
S.update({e:False}); w = wins(v, S, 0) 
