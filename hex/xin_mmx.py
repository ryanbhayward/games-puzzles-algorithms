# return winning move if ptm wins, else None
def mmx_move(psn, ptm): # assumes no winner yet
  optm = oppCH(ptm) # opponent of player-to-move
  for k in CELLS: # for every cell on the board
    if is_empty_cell(k, psn): 
      new_psn = color_cell(k, psn, ptm) 
      if has_win(new_psn, ptm): # did ptm win?
        return k
      # if not, continue from new_psn with optm
      optm_wins = mmx_move(new_psn, optm)
      # if optm has no winning move, then
      #   ptm move at k is a winning move
      if not optm_wins:
        return k
  return None
