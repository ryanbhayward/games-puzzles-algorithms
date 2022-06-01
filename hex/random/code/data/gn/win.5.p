#set terminal epslatex
set terminal post eps
set output "winrate.5.eps"
set key left box
set xrange[5:13]
set yrange[0.0:0.16]
set xlabel "move number"
set ylabel "win rate on that move"
set offsets 0.5, 0.5, 0, 0
#set label "(13, 0.146)" at 13,0.15 center
plot '5.dat' using 1:2 title "Hex 5x5 win rates by move" with impulses
