#!/bin/bash
source ../mypython3.sh
set -x

${mypython3} -B exec2sql1.py eval_save0.sql eval_save0>eval_save0.tto
${mypython3} -B exec2sql1.py eval_save1.sql eval_save1>eval_save1.tto

sqlite3 -header -box ../../x4sqlite1.db <eval_scores0.sql >eval_scores0.txt
sqlite3 -header -box ../../x4sqlite1.db <eval_scores1.sql >eval_scores1.txt
sqlite3 -header -box ../../x4sqlite1.db <eval_scores2.sql >eval_scores2.txt
sqlite3 -header -box ../../x4sqlite1.db <eval_scores3.sql >eval_scores3.txt

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

txt2html2browser eval_scores0.txt
txt2html2browser eval_scores1.txt
txt2html2browser eval_scores2.txt
txt2html2browser eval_scores3.txt
