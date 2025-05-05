# return winning move if ptm wins else empty string
0 def mmx_move(psn, ptm): # assumes no winner yet
1   optm = oppCH(ptm) # opponent of player-to-move
2   for k in CELLS: # for every cell on the board
3     if is_empty_cell(k, psn): 
4       new_psn = color_cell(k, psn, ptm) 
5       if has_win(new_psn, ptm): # did ptm win?
6         return k
7       # if not, continue from new_psn with optm
8       optm_wins = mmx_move(new_psn, optm)
9       # if optm has no winning move, then
10      #   ptm move at k is a winning move
11      if not optm_wins:
12         return k
13  return '' # no winning move
