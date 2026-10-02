source ../mypython3.sh
set -x

#---Np-237
#${mypython3} -B reac2pfns.py -o:pfns237np00_5 -x1:5.2e5 -fx:1e6 -xmin:0.001 -xmax:30 -xlog -lines -sym "93-NP-237(N,F),PR,NU/DE" -annot:"0.02,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np00_5.tto
#${mypython3} -B reac2pfns.py -o:pfns237np00_5 -zdat:np237nf-JENDL-4.0.zvd.dat -x1min:4.9e5 -x1max:6.2e5 -fx:1e6 -xmin:0.02 -xmax:30 -ymin:0.2 -ymax:1.6 -xlog --lines -sym "93-NP-237(N,F),PR,NU/DE" "93-NP-237(N,F),PR,NU/DE,,REL" -annot:"0.2,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np00_5.tto
 ${mypython3} -B reac2pfns.py -o:pfns237np00_5 -zdat:np237nf-JENDL-4.0.zvd.dat -x1:5.2e5 -fx:1e6 -xmin:0.02 -xmax:30 -ymin:0.2 -ymax:1.6 -xlog -lines -sym "93-NP-237(N,F),PR,NU/DE" -annot:"0.2,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np00_5.tto
 ${mypython3} -B reac2pfns.py -o:pfns237np14_7 target:Np-237 -exp1:exp41171004.txt -leg -Ei:14.7e6 -T:1.369e6 -nogrp -x1min:14e6 -x1max:15e6 -xlog -fx:1e6 -xmin:0.03 -xmax:30 -ymin:0.2 -ymax:2.8 -sym -symw=10 "93-NP-237(N,F),PR,NU/DE*" -annot:"0.2,2.7,<sup>237</sup>Np(n<sub>14.7MeV</sub>,f)PFNS (T=1.369MeV)">pfns237np14_7.tto

exit
