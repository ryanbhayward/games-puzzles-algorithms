#set terminal epslatex
set output "winrate21.eps"
set terminal post eps font "Courier,24"
set key left
set xrange[257:441]
set yrange[0.0:0.023]
set offsets 2, 2, 0, 0
plot '21.dat' using 1:2 title "first-player winrates" with impulses
