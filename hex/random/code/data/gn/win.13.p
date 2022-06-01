#set terminal epslatex
set terminal post eps
set output "winrate.13.eps"
set key left box
set xrange[44:126]
set yrange[0.0:0.05]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(85, 0.0365)" at 85,0.04 center
plot '13.dat' using 1:2 title "Hex 13x13 win rates by move" with impulses
