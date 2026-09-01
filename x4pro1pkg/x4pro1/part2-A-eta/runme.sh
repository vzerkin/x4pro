source ../mypython3.sh
set -x

 ${mypython3} -B eta.py u-235 -ylog -xlog -annot:"0.01,6,<b>Eta(MT18)</b>" >eta-u235.tto
#${mypython3} -B eta.py u-235 -t:u-235 -r:"n,abs" -ylog -xlog >eta-u235.tto
 ${mypython3} -B eta.py u-238  -ylog -xlog     >eta-u238.tto
 ${mypython3} -B eta.py u-233  -ylog -xlog     >eta-u238.tto
 ${mypython3} -B eta.py pu-239 -ylog -xlog -annot:"0.1,8,<b>Eta(MT18)</b>"  >eta-pu239.tto
 ${mypython3} -B eta.py u-235  -r:"n,el" -ylog -xlog >eta-u235nel.tto
 ${mypython3} -B eta.py u-238  -r:"n,el" -ylog -xlog >eta-u238nel.tto
 ${mypython3} -B eta.py u-233  -r:"n,el" -ylog -xlog >eta-u233nel.tto
 ${mypython3} -B eta.py pu-239 -r:"n,el" -ylog -xlog >eta-pu239nel.tto
 ${mypython3} -B ../myplot1.py U235-eta -x:log -y:log -o:U235-eta-myplot.html >U235-eta-myplot.tto
 ${mypython3} -B ../myplot1.py U233-eta -x:log -y:log -o:U233-eta-myplot.html >U233-eta-myplot.tto
 ${mypython3} -B ../myplot1.py Pu239-eta -x:log -y:log -o:Pu239-eta-myplot.html >Pu239-eta-myplot.tto

set +x
exit
