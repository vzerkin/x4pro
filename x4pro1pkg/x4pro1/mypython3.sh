#!/bin/bash
#set -x

py3='3'
mypython3="python$py3"

myos=`uname -s`
if test   "$myos" = "Darwin" ; then
    py3='3'	#----MacOS
elif test "$myos" = "Linux" ; then
    py3='3'	#----Linux
else
    py3=''	#----Window/MinGW
    export PYTHONIOENCODING="utf-8"
    export PYTHONLEGACYWINDOWSSTDIO="utf-8"
fi
mypython3="python$py3"
