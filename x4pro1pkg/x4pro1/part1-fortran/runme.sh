#!/bin/bash

source ../mypython3.sh

#set -x

styl1="style=\"padding-left:8px;color:#00f;background-color:#ff0;font-style:italic;border-bottom:1px solid #00f;\""
styl2="style=\"padding-left:8px;color:#00f;background-color:#ff0;font-style:italic;\""

echo "Run program f1.exe on `uname -s`"
./f1.exe >f1.tto
echo "___errCode=$?"
echo "________Result: files sql1tmp.dat f1.tto"
ls -la sql1tmp.dat f1.tto
echo "&nbsp; X4Pro by V.Zerkin, ver.2022-12-21. Running: `date +'%F %T'`">f1.tto.html
echo '<table><tr><td style="vertical-align:top;padding:3pt;border-right:1px solid #777">'>>f1.tto.html
# echo '<div style="padding-left:16px;color:#00f;background-color:#ff0;border-bottom:1px solid #00f;font-style:italic">Program source file: f1.f</div>'>>f1.tto.html
  echo "<div ${styl1}>Program source file: f1.f</div>">>f1.tto.html
  echo '<pre style="margin:0;padding:0;padding-top:3px">'>>f1.tto.html
  cat f1.f|grep -v '^!'>>f1.tto.html
  echo "</pre>" >>f1.tto.html
#  echo '<hr>'>>f1.tto.html
echo '</td><td style="vertical-align:top;padding:3pt">'>>f1.tto.html
  echo "<div ${styl1}>Terminal output: f1.tto</div>">>f1.tto.html
  echo '<pre style="margin:0;padding:0;padding-top:3px">'>>f1.tto.html
  cat f1.tto>>f1.tto.html
  echo "</pre>" >>f1.tto.html
  echo '<br><br>'>>f1.tto.html
#echo '</td><td style="vertical-align:top;padding:3pt">'>>f1.tto.html
  echo "<div ${styl1}>Temporary file: sql1tmp.dat</div>">>f1.tto.html
  echo '<pre style="margin:0;padding:0;padding-top:3px">'>>f1.tto.html
  cat sql1tmp.dat>>f1.tto.html
  echo "</pre>" >>f1.tto.html
#  echo '<hr>'>>f1.tto.html
echo "</td></tr></table>">>f1.tto.html
#exit

${mypython3} -B ../open-webbrowser.py f1.tto.html


echo "Run program dae1e2.exe on `uname -s`"
./dae1e2.exe >dae1e2.tto
echo "___errCode=$?"
echo "________Result: files sql1tmp.dat dae1e2.tto"
ls -la sql1tmp.dat dae1e2.tto
echo "<pre>" >dae1e2.tto.html
cat dae1e2.tto>>dae1e2.tto.html
echo "</pre>" >>dae1e2.tto.html
${mypython3} -B ../open-webbrowser.py dae1e2.tto.html


echo "Run program sig1.exe on `uname -s`"
./sig1.exe >sig1.tto
echo "___errCode=$?"
echo "________Result: files sql1tmp.dat sig1.tto"
ls -la sql1tmp.dat sig1.tto
echo "<pre>" >sig1.tto.html
cat sig1.tto>>sig1.tto.html
echo "</pre>" >>sig1.tto.html
${mypython3} -B ../open-webbrowser.py sig1.tto.html


echo "Run program sig1toc4.exe on `uname -s`"
./sig1toc4.exe >sig1toc4.tto 2>sig1toc4_err.tto
echo "___errCode=$?"
echo "________Result: files sql1tmp.dat sig1toc4.tto sig1toc4.c4"
ls -la sql1tmp.dat sig1toc4.tto sig1toc4.c4
echo "<pre>" >sig1toc4.tto.html
echo -e "\n<span ${styl2}>________File:sig1toc4.c4________</span>\n" >>sig1toc4.tto.html
cat sig1toc4.c4>>sig1toc4.tto.html
echo -e "\n\n\n<span ${styl2}>________File:sig1toc4.tto________</span>\n" >>sig1toc4.tto.html
cat sig1toc4.tto>>sig1toc4.tto.html
echo "</pre>" >>sig1toc4.tto.html
${mypython3} -B ../open-webbrowser.py sig1toc4.tto.html


echo "Run program legrs2da.exe on `uname -s`"
./legrs2da.exe >legrs2da.tto 2>legrs2da_err.tto
echo "___errCode=$?"
echo "________Result: files sql1tmp.dat legrs2da.tto legrs2da.c4"
ls -la sql1tmp.dat legrs2da.tto legrs2da.c4
echo "<pre>" >legrs2da.tto.html
echo -e "\n<span ${styl2}>________File:legrs2da.c4________</span>\n" >>legrs2da.tto.html
cat legrs2da.c4>>legrs2da.tto.html
echo -e "\n\n\n<span ${styl2}>________File:legrs2da.tto________</span>\n" >>legrs2da.tto.html
cat legrs2da.tto>>legrs2da.tto.html
echo -e "\n<span ${styl2}>________File:sql1tmp.dat________</span>\n" >>legrs2da.tto.html
cat sql1tmp.dat>>legrs2da.tto.html
echo "</pre>" >>legrs2da.tto.html
${mypython3} -B ../open-webbrowser.py legrs2da.tto.html


echo ""
