source ../mypython3.sh

if [ -f da0an.html ]; then rm -f da0an.html ; fi

set -x
${mypython3} -B da0an.py show=0 >da0an.tto
set +x
if [ ! -f da0an.html ]; then
    echo "<img src=da0an.png>" >da0an.tto.html
    ${mypython3} -B ../open-webbrowser.py da0an.tto.html
fi
