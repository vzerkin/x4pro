source ../mypython3.sh
set -x

#---2026-09-25 Testing the applicability of algorithms translating EXFOR.DATA --> PFNS Ratio.
#              Option: "-shape" - use "shape re-normalization" even for absolute data,
#                      given in units, like "PT/FIS/MEV" - particles per fission per MeV
#              Note:   by default shape re-normalization is used only for "relative" EXFOR data,
#                      for example, for quantities coded ",PR,NU/DE,,NPD" and ",PR,NU/DE,,REL"
#                      and given in units, like "NO-DIM", "ARB-UNITS", "1/MEV"
 ${mypython3} -B reac2pfns.py -o:pfns239pu_t_abs        -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.5,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)PFNS:abs2ratio" >pfns239pu_t_abs.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu_t_shp -shape -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.5,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)PFNS:shape2ratio" >pfns239pu_t_shp.tto


exit
