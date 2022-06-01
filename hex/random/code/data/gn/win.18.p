#set terminal epslatex
set terminal post eps
set output "winrate.18.eps"
set key left box
set xrange[100:225]
set yrange[0.0:0.029]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(162, 0.0233)" at 162,0.026 center
plot '18.dat' using 1:2 title "Hex 18x18 win rates by move" with impulses
