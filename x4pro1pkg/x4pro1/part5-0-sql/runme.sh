#!/bin/bash
source ../mypython3.sh
set -x

sqlite3 -header -box ../../x4sqlite1.db <eval_scores1.sql >eval_scores1.txt
sqlite3 -header -box ../../x4sqlite1.db <eval_scores2.sql >eval_scores2.txt
sqlite3 -header -box ../../x4sqlite1.db <eval_scores3.sql >eval_scores3.txt

${mypython3} -B err-t.py    >err-t.tto
${mypython3} -B data-err.py >data-err.tto
${mypython3} -B exec1sql.py EN-le0.sql  EN-le0py >EN-le0py.tto
${mypython3} -B exec1sql.py PTY-eq0.sql PTY-eq0  >PTY-eq0.tto

sqlite3 -header -box ../../x4sqlite1.db <sql3.sql >sql3.txt
sqlite3 -header -box ../../x4sqlite1.db <EN-le0.sql >EN-le0.txt
sqlite3 -header -csv ../../x4sqlite1.db <EN-le0.sql >EN-le0.csv

set +x

txt2html2browser()
{
    inFile=$1
    outFile=$1.html
    styl2="style=\"padding-left:8px;color:#00f;background-color:#ff0;font-style:italic;\""

    echo "<pre>" >$outFile
    echo -e "\n<span ${styl2}>________ File:$1 ________`date +%F,%T`</span>\n" >>$outFile
    cat $1 >>$outFile
    echo "</pre>" >>$outFile

    if [ "$2" != "" ]; then
        echo "<pre>" >>$outFile
        echo -e "\n<span ${styl2}>________ File:$2 ________`date +%F,%T`</span>\n" >>$outFile
        cat $2 | sed "s/</\&lt;/g" | sed "s/>/\&gt;/g">>$outFile
        echo "</pre>" >>$outFile
    fi

    ${mypython3} -B ../open-webbrowser.py $outFile
}

txt2html2browser data-err.json
txt2html2browser data-err.csv
txt2html2browser sql3.txt sql3.sql
