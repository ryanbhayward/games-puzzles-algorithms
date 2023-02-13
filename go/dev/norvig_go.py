##   start of go program that uses norvig-sudoku-esque representation

def nbr_set(p):
  c, r = cols.find(p[0]), rows.find(p[1])
  S = set()
  if r > 0:           S.add( cols[c  ] + rows[r-1] )
  if r < len(rows)-1: S.add( cols[c  ] + rows[r+1] )
  if c > 0:           S.add( cols[c-1] + rows[r  ] )
  if c < len(cols)-1: S.add( cols[c+1] + rows[r  ] )
  return S

cols   = 'ABCD'
rows   = '123'
points = [c+r for c in cols for r in rows]
nbrs   = dict((p, nbr_set(p)) for p in points)
