#!/bin/bash
source ../mypython3.sh
set -x
${mypython3} -B fy1e.py Pu-239 Mo-99           >pu239_mo99.tto
#${mypython3} -B fy1e.py U-235 Mo-99           >u235_mo99.tto
${mypython3} -B fy1e.py u-235 kr-85-m log log  >u235_kr85m.tto
${mypython3} -B fy1e.py u-235 cd-115-g log log >u235_cd115g.tto
set +x
