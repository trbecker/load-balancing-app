set term png
set output "latency.png"
set multiplot layout 3,1


set datafile separator ","
set xrange [0:400]
set yrange [0:6000]
unset xlabel
set xtics ('' 0, '' 15, '' 30, '' 100, '' 200, '' 300, '' 400)
set ylabel "RTT (ms)"
set ytics ('' 0, '2000' 2000, '4000' 4000, '' 6000)

set macros
POS = "at graph 0.1,0.9"

set tmargin at screen 0.96
set bmargin at screen 0.68
set label 1 'Experiment 1' @POS
plot 'experiment_1/aggregated.csv' using 0:2 smooth csplines title "Admission RTT",

set tmargin at screen 0.68
set bmargin at screen 0.40
set label 1 'Experiment 2' @POS
plot 'experiment_2/aggregated.csv' using 0:2 smooth csplines title "Admission RTT",

set xlabel "Time (s)"
set xtics ('' 0, '15' 15, '30' 30, '100' 100, '200' 200, '300' 300, '400' 400)
set tmargin at screen 0.40
set bmargin at screen 0.12
set label 1 'Experiment 3' @POS
plot 'experiment_3/aggregated.csv' using 0:2 smooth csplines title "Admission RTT"
