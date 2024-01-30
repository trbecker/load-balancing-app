set term png size 900,450
set output "latency.png"

set datafile separator ","
set xlabel "Time (s)"
set ylabel "RTT (ms)"

set title "Admission RTT"

plot 'experiment_1/aggregated.csv' using 0:2 smooth csplines lw 3 title "No intent", \
     'experiment_2/aggregated.csv' using 0:2 smooth csplines lw 3 title "Intent limiting 1800 UEs per gNB", \
     'experiment_3/aggregated.csv' using 0:2 smooth csplines lw 3 title "Intent limiting requests over time"
