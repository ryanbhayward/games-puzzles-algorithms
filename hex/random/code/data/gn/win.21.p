set terminal post eps font "Courier,20"
set output "winrate.21.eps"
set key font "Courier,24" left
set xrange[259:445]
set yrange[0.0:0.02]
plot '21.dat' using 1:2 title "1st-player win probability by move" with impulses
