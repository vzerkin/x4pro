source ../mypython3.sh
#echo "---par0=[$0]"
#echo "---par1=[$1]"
#echo "---par2=[$2]"
set -x
${mypython3} -B sig1r.py Al-27 n,a -x:log >Al27na.tto
${mypython3} -B sig1r.py Mn-55 n,g -x:log -y:log -g:n >Mn55ng-n.tto
${mypython3} -B sig1r.py Pu-240 n,f -emin:6.5e+6 -emax:23e+6 -g:n >Pu240nf.tto
if [ "$1" = "" ]; then
    #${mypython3} -B sig1r.py Al-27 n,a -x:log -p:"%" >Al27na2.tto
    ${mypython3} -B sig1r.py Zn-64 n,p >zn64np.tto
#   ${mypython3} -B sig1r.py U-235 n,g -x:log -y:log -g:MT -nosort >U235ng.tto
#   ${mypython3} -B sig1r.py U-235 n,g -x:log -y:log -g:n          >U235ng-n.tto
    ${mypython3} -B sig1r.py U-235 n,g -x:log -y:log -g:MT         >U235ng.tto
    #${mypython3} -B sig1r.py Pu-240 n,f -emin:6.5e+6 -emax:23e+6 >Pu240nf.tto
    ${mypython3} -B sig1r.py Mn-55 n,g -x:log -y:log >Mn55ng.tto

fi
${mypython3} -B myplot.py Mn55ng-n -x:log -y:log -o:Mn-55-myplot.html >Mn-55-myplot.tto
${mypython3} -B myplot.py Pu240nf-n -o:Pu240nf-n-myplot.html >Pu240nf-n-myplot.tto
#${mypython3} -B myplot.py U235ng-n -x:log -y:log -o:U235ng-n-myplot.html >U235ng-n-myplot
${mypython3} -B myplot.py U235ng -x:log -y:log -o:U235ng-myplot.html >U235ng-myplot.tto
set +x
