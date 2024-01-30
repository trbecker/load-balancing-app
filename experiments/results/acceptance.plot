set term eps color size 4,6
set output "acceptance_global.eps"
set multiplot layout 3,1

set datafile separator ","
set ylabel "Connections"
set xlabel "Time (s)"

set xrange [0:400]
set yrange [0:65]
set xtics ('' 0, '' 15, '' 30, '' 100, '' 200, '' 300, '' 400)
unset xlabel

set macros
POS = "at graph 0.1,0.9"

set tmargin at screen 0.95
set bmargin at screen 0.65
set label 1 'Experiment 1' @POS
plot 'experiment_1/accepted.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_1/denied.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.65
set bmargin at screen 0.35
set label 1 'Experiment 2' @POS
plot 'experiment_2/accepted.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_2/denied.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.35
set bmargin at screen 0.05
set xtics ('' 0, '15' 15, '30' 30, '100' 100, '200' 200, '300' 300, '' 400)
set xlabel "Time (s)"
set label 1 'Experiment 3' @POS
plot 'experiment_3/accepted.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied.csv' u 1:2 smooth csplines t 'Denied'
