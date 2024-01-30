set term postscript eps size 2.5,4.2 color
set output "gnb2.eps"
set multiplot layout 6,1

set datafile separator ","
set ylabel "Connections"

set yrange [0:20]
set ytics ('' 0, '5' 5, '10' 10, '15' 15, '' 30)
set xtics 100
unset xlabel

set format x ''

set macros
POS = "at graph 0.05,0.8"

set tmargin at screen 0.99
set bmargin at screen 0.83
set label 1 'gnb1' @POS
plot 'experiment_3/accepted_gnb1.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied_gnb1.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.83
set bmargin at screen 0.68
set label 1 'gnb2' @POS
plot 'experiment_3/accepted_gnb2.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied_gnb2.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.68
set bmargin at screen 0.53
set label 1 'gnb3' @POS
plot 'experiment_3/accepted_gnb3.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied_gnb3.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.53
set bmargin at screen 0.38
set label 1 'gnb4' @POS
plot 'experiment_3/accepted_gnb4.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied_gnb4.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.38
set bmargin at screen 0.23
set label 1 'gnb5' @POS
plot 'experiment_3/accepted_gnb5.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied_gnb5.csv' u 1:2 smooth csplines t 'Denied'

set tmargin at screen 0.23
set bmargin at screen 0.08
set format x '%.0f'
set xlabel "Time (s)"
set label 1 'gnb6' @POS
plot 'experiment_3/accepted_gnb6.csv' u 1:2 smooth csplines t 'Accepted', \
     'experiment_3/denied_gnb6.csv' u 1:2 smooth csplines t 'Denied'