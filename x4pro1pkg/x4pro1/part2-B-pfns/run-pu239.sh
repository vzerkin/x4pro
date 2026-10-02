source ../mypython3.sh
set -x

#---Pu-239
 ${mypython3} -B reac2pfns.py -o:pfns239pu00_0th  -zdat:pu239nf-JENDL-5.zvd.dat       -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.3,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)pfns T=1.32MeV" >pfns239pu00_0th.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu00_0th138 -nogrp -T:1.382e6 -zdat:pu239nf-JENDL-5.zvd.dat -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -sym "94-PU-239(N,F),PR,NU/DE,,MXW" "94-PU-239(N,F),PR,NU/DE,,MXD" -annot:"0.3,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)pfns T=1.382MeV" >pfns239pu00_0th138.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu01_45 -zdat:pu239nf-INDEN-Aug2023.zvd.dat -rsp1:F51-18-7.txt -nogrp -x1min:1.45e6 -x1max:1.5e6 -fx:1e6 -xmin:0.02 -xmax:45 -ymin:0.55 -ymax:1.8 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE" "94-PU-239(N,F),PR,NU/DE,,MXD" -annot:"0.25,1.7,<sup>239</sup>Pu(n<sub>1.45MeV</sub>,f) PFNS" >pfns239pu01_45.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu14  -zdat:pu239nf-INDEN-Aug2023.zvd.dat -rsp1:F51-1846.txt -nogrp -Ei:14e6 -x1min:13.9e6 -x1max:14.5e6 -fx:1e6 -xlog -xmin:0.04 -xmax:35 -ymin:0 -ymax:3.5 -sym -annot:"0.4,3.2,<sup>239</sup>Pu(n<sub>14MeV</sub>,f) PFNS" "94-PU-239(N,F),PR,NU/DE" "94-PU-239(N,F),PR,NU/DE,,MXD" "94-PU-239(N,F),PR,NU/DE,,NPD" "94-PU-239(N,F),PR,NU/DE,,REL" >pfns239pu14.tto


exit
