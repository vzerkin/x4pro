source ../mypython3.sh
set -x

#---U-238
 ${mypython3} -B reac2pfns.py -o:pfns238u08_94 -x1:8.94e6 -fx:1e6 -xmin:0.005 -xmax:50 -ymin:0.3 -ymax:2.5 -xlog -lines -sym "92-U-238(N,F),PR,NU/DE" -annot:"0.1,2.3,<sup>238</sup>U(n<sub>8.94MeV</sub>,f) PFNS" >pfns238u08_94.tto
#${mypython3} -B reac2pfns.py -o:pfns238u14_3 -x1:14.3e6 -fx:1e6 -xmin:0.1 -xmax:40 -ymin:0.3 -ymax:3.5 -xlog -lines -sym "92-U-238(N,F),PR,NU/DE" -annot:"1,3.2,<sup>238</sup>U(n<sub>14.3MeV</sub>,f) PFNS">pfns238u14_3.tto
 ${mypython3} -B reac2pfns.py -o:pfns238u14_7 -Ei:14.7e6 -rsp1:F51-1839.txt -nogrp -leg -x1min:14e6 -x1max:15e6 -fx:1e6 -xmin:0.02 -xmax:22 -ymin:0 -ymax:3.5 -xlog -sym "92-U-238(N,F),PR,NU/DE" "92-U-238(N,F),PR,NU/DE,,NPD" "92-U-238(N,F),PR,NU/DE,,REL" -annot:"0.1,3.38,<sup>238</sup>U(n<sub>14.7MeV</sub>,F) PFNS">pfns238u14_7.tto


set +x
exit
