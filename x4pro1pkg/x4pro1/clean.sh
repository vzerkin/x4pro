#set -x
dirnames="*"
ii=0; nftot=0
for dir in $dirnames; do
    if [ ! -d $dir ]; then continue ; fi
    if [ "$dir" = "img"  ] ; then continue; fi
    if [ "$dir" = "doc"  ] ; then continue; fi
    if [ "$dir" = "jsx"  ] ; then continue; fi
    if [ "$dir" = "x4js" ] ; then continue; fi
    ii=$(($ii+1))
#    echo " --clean: $dir"
    printf " --clean-dir:%-3d %-20s " $ii ${dir}
    pushd $dir >/dev/null
#    rm -rf out00/
#    rm -rf out01/
#    rm -f runme3.sh
    if [ -f temp-plot.html ]; then rm -f temp-plot.html ; fi
    if [ -f myBlackList.json ]; then mv myBlackList.json myBlackList-json.save ; fi

#    rm *.tto *.html *.json 2>/dev/null
#    rm *.tto.txt *.htm *.json.txt *.png *.pdf 2>/dev/null
    rmnames="*.html *.htm *.json *.tto *.c4 *.zvd *.r33dat *.pdf *.png sql1tmp.dat *.csv EN-le0.txt sql3.txt eval_scores*.txt"
    nf=`ls -1 ${rmnames} 2>/dev/null|wc -l`
#    echo " --clean: $dir	$nf"
    if [ $nf -gt 0 ] ; then
	printf " %2d files\n" $nf
	nftot=$(($nftot+$nf))
    else
	printf " %-5s\r" ""
    fi
    rm $rmnames 2>/dev/null
#    rm *.*0
    if [ -f myBlackList-json.save ]; then mv myBlackList-json.save myBlackList.json ; fi
    popd >/dev/null
done
#echo ""
printf " --clean-dir:%d  files:%d  %-20s \n" $ii $nftot ""
#set +x
