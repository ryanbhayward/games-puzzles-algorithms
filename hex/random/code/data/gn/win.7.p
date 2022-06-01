#set terminal epslatex
set terminal post eps
set output "winrate.7.eps"
set key left box
set xrange[7:43]
set yrange[0.0:0.1]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(25, 0.0884)" at 25,0.092 center
plot '7.dat' using 1:2 title "Hex 7x7 win rates by move" with impulses
