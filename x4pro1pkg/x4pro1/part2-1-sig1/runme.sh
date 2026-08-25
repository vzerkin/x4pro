source ../mypython3.sh
set -x
${mypython3} -B sig1x.py "" "" log >sig1x1.tto
if [ "$1" == "" ]; then
    ${mypython3} -B sig1x.py "" "" log "" "%"  >sig1x2.tto
    ${mypython3} -B sig1x.py mn-55 n,g log log >sig1x3.tto
    #${mypython3} -B sig1x.py al-27 n,tot log log >sig1x4.tto
fi
set +x
