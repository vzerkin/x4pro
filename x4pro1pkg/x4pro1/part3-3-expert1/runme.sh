source ../mypython3.sh
set -x
#if [ ! -f corr_subr.py ]; then cp -p corr_subr.py00 corr_subr.py ; fi
cp -p corr_subr.py00a corr_subr.py
${mypython3} -B x13597002.py >x12898sig.tto
set +x
