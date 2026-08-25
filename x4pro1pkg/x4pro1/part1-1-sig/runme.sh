#!/bin/bash
source ../mypython3.sh
#echo "===mypython3:${mypython3} pid:$$"
set -x
${mypython3} -B sig0x.py >sig0x.tto
${mypython3} -B sig0x2.py>sig0x2.tto
set +x
