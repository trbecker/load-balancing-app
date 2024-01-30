set term png size 900,450
set output "sinr.png"

set datafile separator ","
set xlabel "Time (s)"
set ylabel "SINR (dB)"

set yrange [80:100]

set title "SINR"

plot 'experiment_1/accepted.csv' using 0:3 smooth csplines lw 3 title "No intent", \
     'experiment_2/accepted.csv' using 0:3 smooth csplines lw 3 title "Intent limiting 1800 UEs per gNB", \
     'experiment_3/accepted.csv' using 0:3 smooth csplines lw 3 title "Intent limiting requests over time"
