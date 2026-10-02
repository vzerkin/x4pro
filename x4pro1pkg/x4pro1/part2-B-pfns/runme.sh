source ../mypython3.sh
set -x

bash run-u233.sh
bash run-u235.sh

 bash run-u233.sh
 bash run-u235.sh
 bash run-u238.sh
 bash run-pu239.sh
 bash run-th232.sh
 bash run-np237.sh
 bash run-pu242.sh
 bash run-test-abs.sh

exit

#---U-233
#if [ 1 = 0 ] ; then

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
#fi



#---U-235
    ${mypython3} -B reac2pfns.py -o:pfns235u00_0th -Ei:0.0253 -T:1.31e6 -x1min:0.0253 -x1max:0.0363 \
	-rsp1:F51-18-1.txt \
	-zdat:u235nf-JENDL-5.zvd.dat \
	-zdat:u235nf-JEFF-4.0.zvd.dat \
	-nogrp \
	-fx:1e6 -xmin:0.002 -xmax:50 -ymin:0.55 -ymax:1.2 \
	-xlog -lines -sym \
	-annot:"0.1,1.15,<sup>235</sup>U(n<sub>th</sub>,f)PFNS" \
	"92-U-235(N,F),PR,NU/DE,,MXD" \
	"92-U-235(N,F),PR,NU/DE,,MXW" \
	"92-U-235(N,F),PR,NU/DE,,MXW/REL" \
    >pfns235u00_0th.tto
#	-zdat:u235nf-ENDF_B-VIII.1.zvd.dat \
#	-zdat:u235nf-Minsk-Actinides.zvd.dat \

 ${mypython3} -B reac2pfns.py -o:pfns235u00_5 -rsp1:F51-18-3.txt -x1min:5e5 -x1max:5.3e5 \
 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.3 -ymax:1.6 -xlog -lines -sym \
 "92-U-235(N,F),PR,NU/DE,,REL" \
 "92-U-235(N,F),PR,NU/DE,,NPD" \
 -annot:"0.2,1.5,<sup>235</sup>U(n<sub>0.5MeV</sub>,f) PFNS">pfns235u00_5.tto

#---235U(N:7.4MeV,F)PFNS
    #${mypython3} -B reac2pfns.py -o:pfns235u07_4 -rsp1:F51-1814.txt -x1min:7e6 -x1max:8e6 -fx:1e6 -xmin:0.01 -xmax:40 -ymin:0.5 -ymax:1.95 -xlog -lines -sym "92-U-235(N,F),PR,NU/DE" -annot:"0.2,1.8,<sup>235</sup>U(n<sub>7.4MeV</sub>,f) PFNS">pfns235u07_4.tto

out="pfns235u07_4"
args=(
#---x1: Ein; x2: Eout
#  -x:x2					# xAxis:=x2, i.e. Eout
   -x1min:7e6 -x1max:8e6			# range on x1, i.e. Ein
   -zdat:u235nf-JENDL-5.zvd.dat			# add zvd.dat from u235nf-JENDL-5 MF5+MF35
#  -zdat:u235nf-JEFF-4.0.zvd.dat		# commented option
   -zdat:u235nf-Minsk-Actinides.zvd.dat		# add my curve from zvd.dat file having many Ein-datasets using interpolation
#  -rsp1:F51-1814.txt -rsp1:F51-1815.txt	# add spectra supplied by V.Maslov for Ein=7 and 7.5 MeV to check interpolation
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

out="pfns235u06_6"
args=(
#---x1: Ein; x2: Eout
#  -x:x2					# xAxis:=x2, i.e. Eout
   -Ei:6.5e6					# Ei for evaluated curves
#  -x1:6.6e6					# x1 value, i.e. Ein.exp
   -x1min:6.2e6 -x1max:7e6			# range on x1, i.e. Ein.exp
#  -zdat:u235nf-JENDL-5.zvd.dat			# add zvd.dat from u235nf-JENDL-5 MF5+MF35
#  -zdat:u235nf-JEFF-4.0.zvd.dat		# commented option
   -zdat:u235nf-Minsk-Actinides.zvd.dat		# add my curve from zvd.dat file having many Ein-datasets using interpolation
   -fx:1e6					# multiplyer for data on xAxis 1e6: eV to MeV
#---plotting options
   -xmin:0.001 -xmax:60 -ymin:0.6 -ymax:2.1	# initial display window
   -xlog					# xAxis: log
   -lines					# connect points by lines
   -sym 					# draw symbols with border
#---annotation: (x,y) position in plot-units and (text)
   -annot:"0.02,1.9,<sup>235</sup>U(n<sub>6.5MeV</sub>,f) PFNS"
#---reaction-code to retrieve:
   "92-U-235(N,F),PR,NU/DE"			#absolute units
)
${mypython3} -B reac2pfns.py -o:${out} "${args[@]}" >${out}.tto


out="pfns235u15"
args=(
#---x1: Ein; x2: Eout
#  -x:x2					# xAxis:=x2, i.e. Eout
   -Ei:15e6					# Ei for evaluated curves
   -x1min:14.6e6 -x1max:15.5e6			# range on x1, i.e. Ein.exp
#  -zdat:u235nf-JENDL-5.zvd.dat			# add zvd.dat from u235nf-JENDL-5 MF5+MF35
#  -zdat:u235nf-JEFF-4.0.zvd.dat		# commented option
   -zdat:u235nf-Minsk-Actinides.zvd.dat		# add my curve from zvd.dat file having many Ein-datasets using interpolation
   -fx:1e6					# multiplyer for data on xAxis 1e6: eV to MeV
   -leg
   -nogrp
#---plotting options
   -xmin:0.04 -xmax:30 -ymin:0 -ymax:3.5	# initial display window
   -xlog					# xAxis: log
   -lines					# connect points by lines
   -sym 					# draw symbols with border
#---annotation: (x,y) position in plot-units and (text)
   -annot:"0.15,3.37,<sup>235</sup>U(n<sub>15MeV</sub>,f) PFNS"
#---reaction-code to retrieve:
   "92-U-235(N,F),PR,NU/DE"			#absolute units
   "92-U-235(N,F),PR,NU/DE,,NPD"
   "92-U-235(N,F),PR,NU/DE,,REL"
)
${mypython3} -B reac2pfns.py -o:${out} "${args[@]}" >${out}.tto



#---U-238
 ${mypython3} -B reac2pfns.py -o:pfns238u08_94 -x1:8.94e6 -fx:1e6 -xmin:0.005 -xmax:50 -ymin:0.3 -ymax:2.5 -xlog -lines -sym "92-U-238(N,F),PR,NU/DE" -annot:"0.1,2.3,<sup>238</sup>U(n<sub>8.94MeV</sub>,f) PFNS" >pfns238u08_94.tto
#${mypython3} -B reac2pfns.py -o:pfns238u14_3 -x1:14.3e6 -fx:1e6 -xmin:0.1 -xmax:40 -ymin:0.3 -ymax:3.5 -xlog -lines -sym "92-U-238(N,F),PR,NU/DE" -annot:"1,3.2,<sup>238</sup>U(n<sub>14.3MeV</sub>,f) PFNS">pfns238u14_3.tto
 ${mypython3} -B reac2pfns.py -o:pfns238u14_7 -Ei:14.7e6 -rsp1:F51-1839.txt -nogrp -leg -x1min:14e6 -x1max:15e6 -fx:1e6 -xmin:0.02 -xmax:22 -ymin:0 -ymax:3.5 -xlog -sym "92-U-238(N,F),PR,NU/DE" "92-U-238(N,F),PR,NU/DE,,NPD" "92-U-238(N,F),PR,NU/DE,,REL" -annot:"0.1,3.38,<sup>238</sup>U(n<sub>14.7MeV</sub>,F) PFNS">pfns238u14_7.tto



#---Pu-239
 ${mypython3} -B reac2pfns.py -o:pfns239pu00_0th  -zdat:pu239nf-JENDL-5.zvd.dat       -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.3,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)pfns T=1.32MeV" >pfns239pu00_0th.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu00_0th138 -nogrp -T:1.382e6 -zdat:pu239nf-JENDL-5.zvd.dat -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" "94-PU-239(N,F),PR,NU/DE,,MXD" -annot:"0.3,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)pfns T=1.382MeV" >pfns239pu00_0th138.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu01_45 -zdat:pu239nf-INDEN-Aug2023.zvd.dat -rsp1:F51-18-7.txt -nogrp -x1min:1.45e6 -x1max:1.5e6 -fx:1e6 -xmin:0.02 -xmax:45 -ymin:0.55 -ymax:1.8 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE" "94-PU-239(N,F),PR,NU/DE,,MXD" -annot:"0.25,1.7,<sup>239</sup>Pu(n<sub>1.45MeV</sub>,f) PFNS" >pfns239pu01_45.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu14  -zdat:pu239nf-INDEN-Aug2023.zvd.dat -rsp1:F51-1846.txt -nogrp -Ei:14e6 -x1min:13.9e6 -x1max:14.5e6 -fx:1e6 -xlog -xmin:0.02 -xmax:35 -ymin:0 -ymax:3 -lines -sym -annot:"0.4,2.7,<sup>239</sup>Pu(n<sub>14MeV</sub>,f) PFNS" "94-PU-239(N,F),PR,NU/DE" "94-PU-239(N,F),PR,NU/DE,,MXD" "94-PU-239(N,F),PR,NU/DE,,NPD" "94-PU-239(N,F),PR,NU/DE,,REL" >pfns239pu14.tto



#---Th-232
 ${mypython3} -B reac2pfns.py -o:pfns232th02_9 -zdat:th232nf-JENDL-4.0.zvd.dat -x1min:2.8e6 -x1max:2.9e6 -fx:1e6 -xlog -xmin:2e-5 -xmax:30 -ymin:0.45 -ymax:1.45 -lines -sym "90-TH-232(N,F),PR,NU/DE,,NPD" "90-TH-232(N,F),PR,NU/DE,,REL" -annot:"0.005,1.35,<sup>232</sup>Th(n<sub>2.9MeV</sub>,f) PFNS">pfns232th02_9.tto
 ${mypython3} -B reac2pfns.py -o:pfns232th14_7 -Ei:14.7e6 -nogrp -leg -x1min:14e6 -x1max:15e6 -fx:1e6 -xmin:0.15 -xmax:32 -ymin:0 -ymax:4.35 -xlog -sym "90-TH-232(N,F),PR,NU/DE" "90-TH-232(N,F),PR,NU/DE,,NPD" "90-TH-232(N,F),PR,NU/DE,,REL" -annot:"0.5,4.2,<sup>232</sup>Th(n<sub>14.7MeV</sub>,f)PFNS">pfns232th14_7.tto



#---Np-237
#${mypython3} -B reac2pfns.py -o:pfns237np00_5 -x1:5.2e5 -fx:1e6 -xmin:0.001 -xmax:30 -xlog -lines -sym "93-NP-237(N,F),PR,NU/DE" -annot:"0.02,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np00_5.tto
#${mypython3} -B reac2pfns.py -o:pfns237np00_5 -zdat:np237nf-JENDL-4.0.zvd.dat -x1min:4.9e5 -x1max:6.2e5 -fx:1e6 -xmin:0.02 -xmax:30 -ymin:0.2 -ymax:1.6 -xlog --lines -sym "93-NP-237(N,F),PR,NU/DE" "93-NP-237(N,F),PR,NU/DE,,REL" -annot:"0.2,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np00_5.tto
 ${mypython3} -B reac2pfns.py -o:pfns237np00_5 -zdat:np237nf-JENDL-4.0.zvd.dat -x1:5.2e5 -fx:1e6 -xmin:0.02 -xmax:30 -ymin:0.2 -ymax:1.6 -xlog -lines -sym "93-NP-237(N,F),PR,NU/DE" -annot:"0.2,1.5,<sup>237</sup>Np(n<sub>0.5MeV</sub>,f) PFNS">pfns237np00_5.tto
#${mypython3} -B reac2pfns.py -target:Np-237 -o:pfns237np14_7 -leg -Ei:14.7e6 -T:1.32e6 -nogrp -x1min:14e6 -x1max:15e6 -fx:1e6 -xmin:0.02 -xmax:30 -ymin:0 -ymax:4.35 -xlog -sym "93-NP-237(N,F),PR,NU/DE*" -annot:"0.1,4.2,<sup>237</sup>Np(n<sub>14.7MeV</sub>,f)PFNS">pfns237np14_7.tto



#---2026-09-25 Testing the applicability of algorithms translating EXFOR.DATA --> PFNS Ratio.
#              Option: "-shape" - use "shape re-normalization" even for absolute data,
#                      given in units, like "PT/FIS/MEV" - particles per fission per MeV
#              Note:   by default shape re-normalization is used only for "relative" EXFOR data,
#                      for example, for quantities coded ",PR,NU/DE,,NPD" and ",PR,NU/DE,,REL"
#                      and given in units, like "NO-DIM", "ARB-UNITS", "1/MEV"
 ${mypython3} -B reac2pfns.py -o:pfns239pu_t_abs        -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.5,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)PFNS:abs2ratio" >pfns239pu_t_abs.tto
 ${mypython3} -B reac2pfns.py -o:pfns239pu_t_shp -shape -rsp1:F51-18-1PU.txt -x1:0.0253 -fx:1e6 -xmin:0.01 -xmax:30 -ymin:0.65 -ymax:1.28 -xlog -lines -sym "94-PU-239(N,F),PR,NU/DE,,MXW" -annot:"0.5,1.23,<sup>239</sup>Pu(n<sub>th</sub>,f)PFNS:shape2ratio" >pfns239pu_t_shp.tto


#---2026-09-26 Testing cases when no experimental data exist
#---Pu-242: only evaluated data (no experimental data)
 ${mypython3} -B reac2pfns.py -o:pfns242pu00_0th -target:Pu-242 -Ei:0.0253 -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0.1 -xmax:30 -xlog -annot:"1,2.3,<sup>242</sup>Pu(n<sub>th</sub>,f)PFNS">pfns242pu00_0th.tto
 ${mypython3} -B reac2pfns.py -o:pfns242pu08   -target:Pu-242   -Ei:8e6    -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0.1 -xmax:30 -xlog -annot:"1,3.3,<sup>242</sup>Pu(n<sub>8MeV</sub>,f)PFNS">pfns242pu08.tto
 ${mypython3} -B reac2pfns.py -o:pfns242pu14_7 -target:Pu-242   -Ei:14.7e6 -T:1.32e6 -zdat:pu242nf-ENDF_B-VIII.1.zvd.dat -fx:1e6 -xmin:0.1 -xmax:30 -xlog -annot:"1,6.4,<sup>242</sup>Pu(n<sub>14.7MeV</sub>,f)PFNS">pfns242pu14_7.tto

exit



#---------test: comparison with data presented in the Article "2025, B.Mouss" Fig.12
out="pfns235u15"
args=(
#---x1: Ein; x2: Eout
#  -x:x2					# xAxis:=x2, i.e. Eout
   -Ei:15e6					# Ei for evaluated curves
   -x1min:14.6e6 -x1max:14.99e6			# range on x1, i.e. Ein.exp
#  -zdat:u235nf-JENDL-5.zvd.dat			# add zvd.dat from u235nf-JENDL-5 MF5+MF35
#  -zdat:u235nf-JEFF-4.0.zvd.dat		# commented option
#  -zdat:u235nf-Minsk-Actinides.zvd.dat		# add my curve from zvd.dat file having many Ein-datasets using interpolation
   -fx:1e6					# multiplyer for data on xAxis 1e6: eV to MeV
   -leg
   -nogrp
#---plotting options
   -xmin:0.147 -xmax:12.5 -ymin:0.6 -ymax:2.2	# initial display window
   -xlog					# xAxis: log
   -lines					# connect points by lines
   -sym 					# draw symbols with border
#---annotation: (x,y) position in plot-units and (text)
   -annot:"0.5,2.15,<sup>235</sup>U(n<sub>15MeV</sub>,f) PFNS"
#---reaction-code to retrieve:
   "92-U-235(N,F),PR,NU/DE"			#absolute units
   "92-U-235(N,F),PR,NU/DE,,NPD"
   "92-U-235(N,F),PR,NU/DE,,REL"
)
${mypython3} -B reac2pfns.py -o:${out} "${args[@]}" >${out}.tto

exit
