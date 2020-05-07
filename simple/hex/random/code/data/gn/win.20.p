#set terminal epslatex
set terminal post eps
set output "winrate.20.eps"
set key left box
set xrange[129:272]
set yrange[0.0:0.024]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(201, 0.0202)" at 201,0.022 center
plot '20.dat' using 1:2 title "Hex 20x20 win rates by move" with impulses
