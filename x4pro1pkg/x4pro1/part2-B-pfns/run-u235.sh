source ../mypython3.sh
set -x

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

set +x
exit
