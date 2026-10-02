source ../mypython3.sh
set -x

#---2026-10-02 Testing cases when no experimental data exist
#---Pu-242: only evaluated data (no experimental data)
#${mypython3} -B reac2pfns.py -o:pfns242pu00_0th -target:Pu-242 -Ei:0.0253 -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0.1 -xmax:30 -xlog -annot:"1,2.3,<sup>242</sup>Pu(n<sub>th</sub>,f)PFNS">pfns242pu00_0th.tto
#${mypython3} -B reac2pfns.py -o:pfns242pu08   -target:Pu-242   -Ei:8e6    -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0.1 -xmax:30 -xlog -ymin:0 -ymax:4.5 -annot:"1,3.75,<sup>242</sup>Pu(n<sub>8MeV</sub>,f)PFNS">pfns242pu08.tto
 ${mypython3} -B reac2pfns.py -o:pfns242pu07   -target:Pu-242   -Ei:7e6    -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:3e-6 -xmax:30 -xlog -ylog -ymin:0.3 -ymax:4.2 -annot:"0.001,3.5,<sup>242</sup>Pu(n<sub>7MeV</sub>,f)pfns">pfns242pu07.tto
#${mypython3} -B reac2pfns.py -o:pfns242pu14_7 -target:Pu-242   -Ei:14.7e6 -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0.1 -xmax:30 -xlog -ymin:0 -ymax:4.5 -annot:"1,3.75,<sup>242</sup>Pu(n<sub>14.7MeV</sub>,f)PFNS">pfns242pu14_7.tto
 ${mypython3} -B reac2pfns.py -o:pfns242pu14_7 -target:Pu-242   -Ei:14.7e6 -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0 -xmax:20 -ymin:0.5 -ymax:3.5 -annot:"6,3.2,<sup>242</sup>Pu(n<sub>14.7MeV</sub>,f)pfns">pfns242pu14_7.tto

exit
