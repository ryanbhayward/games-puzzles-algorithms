#set terminal epslatex
set terminal post eps
set output "winrate.17.eps"
set key left box
set xrange[87:204]
set yrange[0.0:0.03]
set xlabel "move number"
set ylabel "win rate on that move"
set label "(145, 0.0252)" at 145,0.027 center
plot '17.dat' using 1:2 title "Hex 17x17 win rates by move" with impulses
