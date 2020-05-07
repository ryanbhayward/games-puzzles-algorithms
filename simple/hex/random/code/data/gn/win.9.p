#set terminal epslatex
set terminal post eps
set output "winrate.9.eps"
set key left box
set xrange[15:65]
set yrange[0.0:0.08]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(41, 0.0612)" at 41,0.065 center
plot '9.dat' using 1:2 title "Hex 9x9 win rates by move" with impulses
