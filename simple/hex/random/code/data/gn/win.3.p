#set terminal epslatex
set terminal post eps
set output "winrate.3.eps"
set key left box
set xrange[2:8]
set yrange[0.0:0.4]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(5, 0.333)" at 5,0.35 center
plot '3.dat' using 1:2 title "Hex 3x3 win rates by move" with impulses
