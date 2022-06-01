#set terminal epslatex
set terminal post eps
set output "winrate.15.eps"
set key left box
set xrange[63:163]
set yrange[0.0:0.04]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(113, 0.0299)" at 113,0.035 center
plot '15.dat' using 1:2 title "Hex 15x15 win rates by move" with impulses
