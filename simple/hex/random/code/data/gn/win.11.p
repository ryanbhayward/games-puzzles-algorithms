#set terminal epslatex
set terminal post eps
set output "winrate.11.eps"
set key left box
set xrange[20:100]
set yrange[0.0:0.06]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(61, 0.0460)" at 61,0.05 center
plot '11.dat' using 1:2 title "Hex 11x11 win rates by move" with impulses
