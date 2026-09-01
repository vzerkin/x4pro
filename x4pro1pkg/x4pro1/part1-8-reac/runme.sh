source ../mypython3.sh
set -x
sqlite3 -header -box ../../x4sqlite1.db <reactions1.sql >reactions1.txt
#sqlite3 -header -box ../../tmp1full/x4sqlite1.db <reactions1.sql >reactions1.txt
#${mypython3} -B reac1.py -o:sig1 -x1max:30e6 -fx:1e6 -fy:1e-3 -lines -sym -annot:"7,180,<b>SIG</b>" "13-AL-27(N,A)11-NA-24,,SIG">sig1.tto
#${mypython3} -B reac1.py -o:da1a -x:x2 -x1min:13.6e6 -x1max:14.7e6 -lines -sym -ylog -fy:1e-3 -annot:"60,1e3,<b>DA(A)</b>" "8-O-16(N,EL)8-O-16,,DA">da1a.tto
#${mypython3} -B reac1.py -o:da1e -x:x1 -x1max:6.5e6 -x2min:160 -x2max:170 -lines -sym -ylog -fx:1e3 -fy:1e-3 -annot:"2500,250,<b>DA(E)</b> <sup>14</sup>N(a,a')" "7-N-14(A,EL)7-N-14,,DA">da1e.tto
#${mypython3} -B reac1.py -o:de1  -x:x2 -x1min:6e6 -fx:1e6 -fy:1e-9 -lines -sym -ylog -annot:"8,3e3,<b>DE</b>" "90-TH-232(N,X)0-NN-1,,DE">de1.tto
#${mypython3} -B reac1.py -o:dae1 -x:x2 -x1min:14.1e6 -x1max:14.2e6 -x3min:45 -x3max:45 -fx:1e6 -fy:1e-9 -ylog -lines -sym -annot:"3,65,<b>DAE</b>" "9-F-19(N,X)0-NN-1,,DA/DE">dae1.tto
#${mypython3} -B reac1.py -o:da1p -x3min:149.5 -x3max:150.5 -lines -sym -fx:1e3 -fy:1e-3 -annot:"2e3,5.6,<b>DA/Partial</b>" "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#${mypython3} -B reac1.py -o:da1p -x2fam:"LVL" -x3min:149.5 -x3max:150.5 -lines -sym -fx:1e3 -fy:1e-3 -annot:"2e3,5.6,<b>DA/Partial</b>" "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#${mypython3} -B reac1.py -o:fy1  -x:x2 -x1min:14e6 -x1max:15e6 -lines -sym -ylog -annot:"75,0.06,<b>FY</b>" "92-U-238(N,F)MASS,CHN,FY">fy1.tto
 ${mypython3} -B reac1.py -o:cst1  -x:x1 -lines -sym -ylog -xlog -fx:1e-3 -annot:"0.5,7.5,<b>SIG/Temp</b>" "82-PB-0(N,TOT),,SIG/TMP">cst1.tto
 ${mypython3} -B reac1.py -o:nu1  -x:x1 -lines -sym -ylog -xlog -fx:1e6 -annot:"3,11.5,<b>NUBAR</b>" "92-U-238(N,F),PR,NU">nu1.tto
 ${mypython3} -B reac1.py -o:tke1 -x:x2 -fy:1e6 -lines -sym -annot:"80,180,<b>TKE</b>" "92-U-235(N,F)MASS,PRE,KE,LF+HF" "92-U-235(N,F)MASS,PRE,KE,LF+HF,MXW">tke1.tto
#${mypython3} -B reac1.py -o:eta1 -x:x1 -x1max:4 -lines -sym -ylog -annot:"0.75,3.25,<b>ETA</b>" "92-U-235(N,ABS),,ETA">eta1.tto
 ${mypython3} -B reac1.py -o:eta2 -x:x1 -lines -sym -ylog -xlog -annot:"0.1,3.5,<b>Eta: ABS+NON</b>" "92-U-235(N,ABS),,ETA" "92-U-235(N,NON),,ETA">eta2.tto
 ${mypython3} -B reac1.py -o:sig1p -x1max:10e6 -x2:478e3 -fx:1e6 -ylog -lines -sym -annot:"2,0.31,<b>SIG/Partial</b>" "3-LI-7(N,INL)3-LI-7,PAR,SIG">sig1p.tto
 ${mypython3} -B reac1.py -o:si28nn -fx:1e6 -xlog -xmin:1 -xmax:21 -lines -sym -annot:"10.4,1.3,<b>DATA and DATA-MIN</b>" "14-SI-28(N,INL)14-SI-28,,SIG">si28nn.tto
 ${mypython3} -B reac1.py -o:a1495-li6 -ds:"a1495*" -fx:1e6 -fy:1e-3 -lines -sym -annot:"1.4,8.5,<b>A1495.x4:3-Li-6*,da</b>" "3-li-6*da">a1495-li6.tto
 ${mypython3} -B reac1.py -o:a1495 -ds:"a1495*" -fx:1e6 -fy:1e-3 -lines -sym -annot:"1.4,8.5,<b>A1495.x4:*,da</b>" "*,DA">a1495.tto
 ${mypython3} -B reac1.py -o:Kokkoris -a1:"Kokkoris" -xlog -ylog -fx:1e6 -fy:1e-3 -lines -sym "*,,DA" -annot:"1.6,350,<b>A1:Kokkoris  R:*,,DA</b>">Kokkoris.tto
 ${mypython3} -B reac1.py -o:sig1prod -fx:1e6 -fy:1e-3 -xlog -lines -sym "92-U-238(P,*)*,*,SIG" "92-U-0(P,*)*,*,SIG" -w:" and (prod like '40-Zr-97' or outParticles like '%zr-97%')">sig1prod.tto

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

txt2html2browser reactions1.txt reactions1.sql



#---tests used for development
#python -B reac1.py -o:sig1par -x1max:10e6 -fx:1e6 -ylog -lines -sym "3-LI-7(N,INL)3-LI-7,PAR,SIG">sig1par.tto
#python -B reac1.py -o:si28nn -lines -sym "14-SI-28(N,INL)14-SI-28,,SIG">si28nn.tto
#python -B reac1.py -o:sig1par -x2fam:"LVL;EXC" -fx:1e6 -ylog -lines "11-NA-23(N,INL)11-NA-23,PAR,SIG">sig1par.tto
#python -B reac1.py -o:sig1par -x2fam:"LVL" -x2min:0.439e6 -x2max:0.441e6 -fx:1e6 -ylog -lines "11-NA-23(N,INL)11-NA-23,PAR,SIG">sig1par.tto
#python -B reac1.py -o:sig1par -x2fam:"LVL" -x2min:0.439e6 -x2max:0.441e6 -fx:1e6 -ylog -xlog -lines "11-NA-23(N,INL)11-NA-23,PAR,SIG">sig1par.tto
#python -B reac1.py -o:tke1 -x:x2 -fy:1e6 -lines -sym -annot:"80,180,<b>TKE</b>" "92-U-235(N,F)MASS,PRE,KE,LF+HF" "92-U-235(N,F)MASS,PRE,KE,LF+HF,MXW">tke1.tto

#python -B reac1.py -o:da1p -x:x3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x:x3 -nmin:3 -x2min:2.9e6 -x2max:2.9e6 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x:x3 -nmin:3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x2fam:"LVL" -x:x3 -nmin:3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x2fam:"LVL" -x:x3 -x1:1.163e6 -nmin:3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x2fam:"LVL" -x:x3 -x2:16.6e6 -nmin:3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x2fam:"LVL" -x:x3 -x2:2.9e6 -nmin:3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x2fam:"LVL" -x:x3 -a1:gould -nmin:3 -ylog -lines -sym -fy:1e-3 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1p -x2fam:"LVL" -x:x3 -a1:gould -nmin:3 -ylog -lines -sym -fy:1e-3 -fx:57.296 "3-LI-6(HE3,P)4-BE-8,PAR,DA">da1p.tto
#python -B reac1.py -o:da1a -ds:"A1495002;A1495003" -lines -sym -fy:1e-3>aa2.tto
#python -B reac1.py -o:da1a -x:x3 -ds:"F0001002" -ylog -lines -sym -fy:1e-3 -fx:57.296>aa2.tto
#python -B reac1.py -o:da1a -x:x2 -nmin:12 -lines -sym -ylog -fy:1e-3 -annot:"60,1e3,<b>DA(A)</b>" "8-O-16(N,EL)8-O-16,,DA">da1a.tto

#python -B reac1.py -o:sig1prod -x2:40097 -fx:1e6 -fy:1e-3 -xlog -ylog -lines -sym "92-U-238(P,*)*,*,SIG" "92-U-0(P,*)*,*,SIG">sig1prod.tto
#python -B reac1.py -o:sig1prod -fx:1e6 -fy:1e-3 -xlog -lines -sym "92-U-238(P,*)*,*,SIG" "92-U-0(P,*)*,*,SIG" -w:" and (prod like '40-Zr-97' or outParticles like '%zr-97%')">sig1prod.tto
#python -B ../myplot1.py sig1prod -x:log -o:sig1prod-myplot.html
