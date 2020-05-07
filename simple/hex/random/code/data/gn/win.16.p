#set terminal epslatex
set terminal post eps
set output "winrate.16.eps"
set key left box
set xrange[70:190]
set yrange[0.0:0.035]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(128, 0.0273)" at 128,0.03 center
plot '16.dat' using 1:2 title "Hex 16x16 win rates by move" with impulses
