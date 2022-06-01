#set terminal epslatex
set terminal post eps font "Courier,24"
set output "winrate11.eps"
set key left box
set xrange[11:61]
set yrange[0.0:0.06]
set xlabel "move number"
set ylabel "win rate on move"
set offsets 2, 2, 0, 0
plot '11.dat' using 1:2 title "11x11 random Hex winrates" with impulses
