source ../mypython3.sh

set -x
${mypython3} -B fy0x.py >fy0x.tto

${mypython3} -B me0plt2d.py >me0plt2d.tto

${mypython3} -B me0mpl3d.py show=0 >me0mpl3d.tto
echo "<img src=me0mpl3d.png>" >me0mpl3d.tto.html
${mypython3} -B ../open-webbrowser.py me0mpl3d.tto.html

${mypython3} -B me0mpl2d2.py show=0 >me0mpl2d2.tto
echo "<img src=me0mpl2d2.png>" >me0mpl2d2.tto.html
${mypython3} -B ../open-webbrowser.py me0mpl2d2.tto.html
set +x
