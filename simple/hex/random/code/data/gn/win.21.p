#set terminal epslatex
set terminal post eps
set output "winrate.21.eps"
set key left box
set xrange[145:298]
set yrange[0.0:0.023]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(222, 0.0189)" at 222,0.021 center
plot '21.dat' using 1:2 title "Hex 21x21 win rates by move" with impulses
