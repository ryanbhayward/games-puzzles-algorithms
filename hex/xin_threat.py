# return winning move if any and union of winner's threats
0 def threat_search(psn, ptm, mustplay): # assumes no winner yet
1   opt = oppCH(ptm) # opponent of player-to-move
1a  u_threats = set() # union of cells of opt threats
2   while mustplay: # mustplay is not empty
3     k = mustplay.pop() # remove cell k from mustplay
4     new_psn = color_cell(k, psn, ptm) 
5     if has_win(new_psn, ptm): # did ptm win?
6       return k, set([k])
7     # if not, continue from new_psn with opt
7a    opt_mp = emptycells(new_psn)
8     opt_mv, threat = threat_search(new_psn, opt, opt_mp)
9     # if opt has no winning move, then
10    #   ptm move at k is a winning move
11    if not opt_mv: # opt loses
11a     threat.add(k)
12      return k, threat
12a   mustplay = mustplay.intersection(threat)
12b   u_threat = u_threats.union(threat)
13  return '', u_threats # no winning move
