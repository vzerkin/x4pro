source ../mypython3.sh

set -x

${mypython3} -B covar1.py show=0 >covar1.tto
echo "<img src=covar1.png>" >covar1.tto.html
${mypython3} -B ../open-webbrowser.py covar1.tto.html

${mypython3} -B covar2.py show=0 >covar2.tto
echo "<img src=covar2.png>" >covar2.tto.html
${mypython3} -B ../open-webbrowser.py covar2.tto.html

set +x
