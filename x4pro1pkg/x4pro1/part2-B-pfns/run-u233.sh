source ../mypython3.sh
set -x

 ${mypython3} -B reac2pfns.py -o:pfns233u00_0th -T:1.34e6 -x1min:0.0253 -x1max:0.0363 -fx:1e6 -xmin:0.002 -xmax:30 -ymin:0.7 -ymax:1.2 -xlog -lines -sym "92-U-233(N,F),PR,NU/DE,,MXD" "92-U-233(N,F),PR,NU/DE" -annot:"0.04,1.17,<sup>233</sup>U(n<sub>th</sub>,f)pfns">pfns233u00_0th.tto

 ${mypython3} -B reac2pfns.py -o:pfns233u00_5 -x1:0.55e6 -fx:1e6 \
   -zdat:u233nf-ENDF_B-VIII.1.zvd.dat \
   -xmin:0.002 -xmax:50 -ymin:0.55 -ymax:1.4 \
   -xlog -lines -sym \
   -annot:"0.1,1.35,<sup>233</sup>U(n<sub>0.5MeV</sub>,f)PFNS" \
   "92-U-233(N,F),PR,NU/DE" \
   "92-U-233(N,F),PR,NU/DE,,MXD" \
   "92-U-233(N,F),PR,NU/DE,,REL" \
   >pfns233u00_5.tto

# use -bw : black-white experimental points

set +x
exit
