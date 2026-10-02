source ../mypython3.sh
set -x

#---Th-232
 ${mypython3} -B reac2pfns.py -o:pfns232th02_9 -zdat:th232nf-JENDL-4.0.zvd.dat -x1min:2.8e6 -x1max:2.9e6 -fx:1e6 -xlog -xmin:2e-5 -xmax:30 -ymin:0.45 -ymax:1.45 -lines -sym "90-TH-232(N,F),PR,NU/DE,,NPD" "90-TH-232(N,F),PR,NU/DE,,REL" -annot:"0.005,1.35,<sup>232</sup>Th(n<sub>2.9MeV</sub>,f) PFNS">pfns232th02_9.tto
 ${mypython3} -B reac2pfns.py -o:pfns232th14_7 -Ei:14.7e6 -nogrp -leg -x1min:14e6 -x1max:15e6 -fx:1e6 -xmin:0.15 -xmax:32 -ymin:0 -ymax:4.35 -xlog -sym "90-TH-232(N,F),PR,NU/DE" "90-TH-232(N,F),PR,NU/DE,,NPD" "90-TH-232(N,F),PR,NU/DE,,REL" -annot:"0.5,4.2,<sup>232</sup>Th(n<sub>14.7MeV</sub>,f)PFNS">pfns232th14_7.tto

exit
