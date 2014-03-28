unset log
unset label
set title "Team Japanese number of weekly logs 2014" font "Verdana, 14"
set datafile separator ","
set y2range [0:100]
set grid ytics xtics
set xrange [0:53]
set xtics 5
set xtics add ("Start" 0)
set xtics add ("End" 53)
set xlabel "Week" font "Verdana"
set nokey
set terminal pngcairo dashed size 1000, 700
set output "tj_logs.png"

plot \
"tjstats.dat" using 1:3 with linespoints lc rgb '#5f99cf' lt 1 lw 2 pt 0 ps 0 axes x1y2
