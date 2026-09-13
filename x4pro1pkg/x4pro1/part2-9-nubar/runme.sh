source ../mypython3.sh
set -x

#${mypython3} -B nubar.py >nubar0.tto
${mypython3} -B nubar.py -xmin:-1 -xmax:34 -ymin:1.5 -ymax:7.5 >nubar0.tto
${mypython3} -B nubar.py -q:dl -ylog -xmax:21 -ymin:0.006 -ymax:0.024 >nubar1.tto
${mypython3} -B nubar.py -q:tot -ylog >nubar2.tto
${mypython3} -B nubar.py U-238 -q:pr -xmin:1 -xmax:35 -ymin:2.2 -ymax:7 -xlog >nubar3.tto
${mypython3} -B nubar.py U-238 -q:dl -xlog -ylog -xmin:0.8 -xmax:35 >nubar4.tto
${mypython3} -B nubar.py U-238 -q:tot >nubar5.tto

set +x
exit

#python -B nubar.py U-238 -q:pr -xmin:1 -xmax:35 -ymin:2.2 -ymax:7 -xlog >nubar3.tto
#python -B nubar.py U-238 -q:dl >nubar2.tto
#python -B nubar.py U-238 -q:tot >nubar2.tto
#python -B nubar.py U-233        >nubar3p.tto
#python -B nubar.py U-233 -q:dl  >nubar3d.tto
#python -B nubar.py U-233 -q:tot >nubar3t.tto
#python -B nubar.py -q:dl -ylog -xmax:21 -ymin:0.006 -ymax:0.024 >nubar1.tto

python -B nubar.py U-233  -q:tot -ylog >nubar2.tto
python -B nubar.py U-235  -q:tot -ylog >nubar2.tto
python -B nubar.py U-238  -q:tot -ylog >nubar2.tto
python -B nubar.py Pu-239 -q:tot -ylog >nubar6.tto
exit

python -B nubar.py U-233  -o:U-233nf-nu  -q:tot -ylog >nubar2.tto
python -B nubar.py U-235  -o:U-235nf-nu  -q:tot -ylog >nubar2.tto
python -B nubar.py U-238  -o:U-238nf-nu  -q:tot -ylog >nubar2.tto
python -B nubar.py Pu-239 -o:Pu-239nf-nu -q:tot -ylog >nubar6.tto
python -B nubar.py Np-237 -o:Np-237nf-nu -q:tot -ylog >nubar6.tto
exit
