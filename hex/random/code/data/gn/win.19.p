#set terminal epslatex
set terminal post eps
set output "winrate.19.eps"
set key left box
set xrange[119:248]
set yrange[0.0:0.026]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(181, 0.0217)" at 181,0.023 center
plot '19.dat' using 1:2 title "Hex 19x19 win rates by move" with impulses
