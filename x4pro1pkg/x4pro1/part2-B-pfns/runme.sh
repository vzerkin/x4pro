source ../mypython3.sh
set -x

#if [ 1 = 0 ] ; then
#---U-233
 ${mypython3} -B reac2pfns.py -o:pfns233u_t -x:x2 -T:1.34e6 -x1min:0.0253 -x1max:0.0363 -fx:1e6 -xmin:0.002 -xmax:30 -ymin:0.7 -ymax:1.2 -xlog -lines -sym "92-U-233(N,F),PR,NU/DE,,MXD" "92-U-233(N,F),PR,NU/DE" -annot:"0.04,1.17,<sup>233</sup>U(n<sub>thermal</sub>,f) PFNS">pfns233u_t.tto

 ${mypython3} -B reac2pfns.py -o:pfns233u0_5 -x:x2 -x1:0.55e6 -fx:1e6 \
   -zdat:u233nf-ENDF_B-VIII.1.zvd.dat \
   -xmin:0.002 -xmax:50 -ymin:0.55 -ymax:1.4 \
   -xlog -lines -sym \
   -annot:"0.1,1.35,<sup>233</sup>U(n<sub>0.5MeV</sub>,f)PFNS" \
   "92-U-233(N,F),PR,NU/DE" \
   "92-U-233(N,F),PR,NU/DE,,MXD" \
   "92-U-233(N,F),PR,NU/DE,,REL" \
   >pfns233u0_5.tto
# use -bw : black-white experimental points
#fi


#---U-235
    ${mypython3} -B reac2pfns.py -o:pfns235u_t -x:x2 -Ei:0.0253 -T:1.31e6 -x1min:0.0253 -x1max:0.0363 \
	-rsp1:F51-18-1.txt \
	-zdat:u235nf-JENDL-5.zvd.dat \
	-zdat:u235nf-JEFF-4.0.zvd.dat \
	-nogrp \
	-fx:1e6 -xmin:0.002 -xmax:50 -ymin:0.55 -ymax:1.2 \
	-xlog -lines -sym \
	-annot:"0.1,1.15,<sup>235</sup>U(n<sub>thermal</sub>,f)PFNS" \
	"92-U-235(N,F),PR,NU/DE,,MXD" \
	"92-U-235(N,F),PR,NU/DE,,MXW" \
    >pfns235u_t.tto
#	-zdat:u235nf-ENDF_B-VIII.1.zvd.dat \
#	-zdat:u235nf-Minsk-Actinides.zvd.dat \

 ${mypython3} -B reac2pfns.py -o:pfns235u0_5 -rsp1:F51-18-3.txt -x:x2 -x1min:5e5 -x1max:5.3e5 \
 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.3 -ymax:1.6 -xlog -lines -sym \
 "92-U-235(N,F),PR,NU/DE,,REL" \
 "92-U-235(N,F),PR,NU/DE,,NPD" \
 -annot:"0.2,1.5,<sup>235</sup>U(n<sub>0.5MeV</sub>,f) PFNS">pfns235u0_5.tto

#---235U(N:7.4MeV,F)PFNS
    #${mypython3} -B reac2pfns.py -o:pfns235u7_4 -rsp1:F51-1814.txt -x:x2 -x1min:7e6 -x1max:8e6 -fx:1e6 -xmin:0.01 -xmax:40 -ymin:0.5 -ymax:1.95 -xlog -lines -sym "92-U-235(N,F),PR,NU/DE" -annot:"0.2,1.8,<sup>235</sup>U(n<sub>7.4MeV</sub>,f) PFNS">pfns235u7_4.tto

out="pfns235u7_4"
args=(
#---x1: Ein; x2: Eout
   -x:x2					# xAxis:=x2, i.e. Eout
   -x1min:7e6 -x1max:8e6			# range on x1, i.e. Ein
   -zdat:u235nf-JENDL-5.zvd.dat			# add zvd.dat from u235nf-JENDL-5 MF5+MF35
#  -zdat:u235nf-JEFF-4.0.zvd.dat		# commented option
   -zdat:u235nf-Minsk-Actinides.zvd.dat		# add my curve from zvd.dat file having many Ein-datasets using interpolation
#  -rsp1:F51-1814.txt -rsp1:F51-1815.txt	# add spectra supplied by V.Maslov for Ein=7 and 7.5 MeV
   -fx:1e6					# multiplyer for data on xAxis 1e6: eV to MeV
#---plotting options
   -xmin:0.01 -xmax:40 -ymin:0.5 -ymax:1.95	# initial display window
   -xlog					# xAxis: log
   -lines					# connect points by lines
   -sym 					# draw symbols with border
#---annotation: (x,y) position in plot-units and (text)
   -annot:"0.2,1.9,<sup>235</sup>U(n<sub>7.4MeV</sub>,f) PFNS"
#---reaction-code to retrieve:
   "92-U-235(N,F),PR,NU/DE"			#absolute units
)
${mypython3} -B reac2pfns.py -o:${out} "${args[@]}" >${out}.tto


#---U-238
 ${mypython3} -B reac2pfns.py -o:pfns238u8_94 -x:x2 -x1:8.94e6 -fx:1e6 -xmin:0.005 -xmax:50 -ymin:0.3 -ymax:2.5 -xlog -lines -sym "92-U-238(N,F),PR,NU/DE" -annot:"0.1,2.3,<sup>238</sup>U(n<sub>8.94MeV</sub>,f) PFNS" >pfns238u8_94.tto
 ${mypython3} -B reac2pfns.py -o:pfns238u14_3 -x:x2 -x1:14.3e6 -fx:1e6 -xmin:0.1 -xmax:40 -ymin:0.3 -ymax:3.5 -xlog -lines -sym "92-U-238(N,F),PR,NU/DE" -annot:"1,3.2,<sup>238</sup>U(n<sub>14.3MeV</sub>,f) PFNS">pfns238u14_3.tto


#---Pu-239
 ${mypython3} -B reac2pfns.py -o:pfns239pu_t   -x:x2 -zdat:pu239nf-JENDL-5.zvd.dat       -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.1,1.23,<sup>239</sup>Pu(n<sub>thermal</sub>,f) PFNS" >pfns239pu_t.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu1_45 -x:x2 -zdat:pu239nf-INDEN-Aug2023.zvd.dat -rsp1:F51-18-7.txt -nogrp -x1min:1.45e6 -x1max:1.5e6 -fx:1e6 -xmin:0.02 -xmax:45 -ymin:0.55 -ymax:1.8 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE" "94-PU-239(N,F),PR,NU/DE,,MXD" -annot:"0.25,1.7,<sup>239</sup>Pu(n<sub>1.45MeV</sub>,f) PFNS" >pfns239pu1_45.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu14   -x:x2 -zdat:pu239nf-INDEN-Aug2023.zvd.dat -rsp1:F51-1846.txt -nogrp -Ei:14e6 -x1min:13.9e6 -x1max:14.5e6 -fx:1e6 -xlog -xmin:0.02 -xmax:35 -ymin:0.1 -ymax:3.3 -lines -sym -annot:"0.4,2.7,<sup>239</sup>Pu(n<sub>14MeV</sub>,f) PFNS" "94-PU-239(N,F),PR,NU/DE" "94-PU-239(N,F),PR,NU/DE,,MXD" "94-PU-239(N,F),PR,NU/DE,,NPD" "94-PU-239(N,F),PR,NU/DE,,REL" >pfns239pu14.tto


#---Th-232
#${mypython3} -B reac2pfns.py -o:pfns232th2_6 -x:x2 -x1:2.6e6 -fx:1e6 -xlog -lines -sym "90-TH-232(N,F),PR,NU/DE,,REL" -annot:"1e-7,3.2,<sup>232</sup>Th(n<sub>2.6MeV</sub>,f) PFNS">pfns232th2_6.tto
 ${mypython3} -B reac2pfns.py -o:pfns232th2_6 -x:x2 -zdat:th232nf-JENDL-4.0.zvd.dat -x1min:2.8e6 -x1max:2.9e6 -fx:1e6 -xlog -xmin:2e-5 -xmax:30 -ymin:0.45 -ymax:1.45 -lines -sym "90-TH-232(N,F),PR,NU/DE,,NPD" "90-TH-232(N,F),PR,NU/DE,,REL" -annot:"0.005,1.35,<sup>232</sup>Th(n<sub>2.9MeV</sub>,f) PFNS">pfns232th2_6.tto


#---Np-237
#${mypython3} -B reac2pfns.py -o:pfns237np0_5 -x:x2 -x1:5.2e5 -fx:1e6 -xmin:0.001 -xmax:30 -xlog -lines -sym "93-NP-237(N,F),PR,NU/DE" -annot:"0.02,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np0_5.tto
 ${mypython3} -B reac2pfns.py -o:pfns237np0_5 -x:x2 -zdat:np237nf-JENDL-4.0.zvd.dat -x1:5.2e5 -fx:1e6 -xmin:0.001 -xmax:30 -xlog -lines -sym "93-NP-237(N,F),PR,NU/DE" -annot:"0.02,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np0_5.tto

exit
