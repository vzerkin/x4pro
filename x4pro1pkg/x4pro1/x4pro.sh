#!/bin/bash
#set -x

# Author:  Viktor Zerkin <v.zerkin@gmail.com>
# Created: February 13, 2026
# License: MIT

mypython3="python3"
prompt="x4pro>"
#dir=`pwd`;dir=${dir##*/}
#prompt="${dir}/x4pro>"

#---Local EXFOR-database
dbfile="../x4sqlite1.db"

#---EXFOR-Statistics output
limitTargets=8
limitProjectiles=8
limitReactions=0
limitQuantity=8

#---Examples
declare -a examples	#runme.sh files
declare -a contents	#runme.sh files
maxExample=0
nExamples=0
declare -a arr_pdir=("part1" "part2" "part3" "part4" "part5" "part6")
declare -a arr_ptxt=(
    "Retrieve and plot EXFOR data"
    "Retrieve and plot EXFOR data and ENDF data from Web"
    "EXFOR data renormalizations, corrections and recalculations"
    "Export contents of X4Pro to NoSQL databases"
    "Find mistakes in EXFOR library //EXFOR compilers"
    "Ratios to CS, Renormalization, Flags and scores //evaluators"
)

setPython3() {
#	python --version >/dev/null 2>/dev/null
#	if [ $? -ne 0 ]; then py3='3'
#	else py3=''
#	fi
#	mypython3="python$py3"
	source mypython3.sh
#	echo "---mypython3:${mypython3} pid:$$"
}

outWelcome() {
    cat x4pro.txt1
    cat <<-EOF
	   +------------------------------------------+
	   | X4Pro: fully relational EXFOR database.  |
	   |         Professional Edition.            |
	   |          Version 2026-02-23.             |
	   |  Demo-examples on Python/SQL/Fortran:    |
	   | search/retrieve/plot/recalculate data.   |
	   | v.zerkin@gmail.com, IAEA-NRDC, 2021-2026 |
	   +------------------------------------------+
	EOF
}

outPlatform() {
    echo "   Run:         `date +'%F,%T'`"
    cat <<-EOF
	   Platform:    `uname -s -m -r`
	   Computer:    `uname -n`
	   Shell:       `bash --version|head -n 1`
	   Bash-ver:    $BASH_VERSION
	   Script:      $0
	   Now Dir:     `pwd`
	EOF
}

outVersions() {
    echo "   ---Versions---"
    ${mypython3} -B versions.py
    echo "   9) gfortran:    `gfortran --version |head -n 1`"
    echo "  10) sqlite3:     `sqlite3 --version | awk '{print $1" "$2" "$3" "$5}'`"
    if command -v dialog >/dev/null; then vdialog=`dialog --version 2>/dev/null`
    else vdialog="-not available-"
    fi
    echo "  11) dialog:      $vdialog"
#	FLSIZE=`du -h "${dbfile}" | cut -f1`
	FLSIZE=`ls -lah "${dbfile}" | awk '{print $5}'`
	FLDATE=`date -r ${dbfile} "+%Y-%m-%d"`
	updated=`sqlite3 ${dbfile} "select max(UpdateDate) from X4UPDATE where UpdateFlag='O'"`
	updated="${updated// /,}"
	nEntry=`sqlite3 ${dbfile} "select count(*) from ENTRY"`
	nDatasets=`sqlite3 ${dbfile} "select count(*) from REACODE where (nDataLines>0)"`
	nPoints=`sqlite3 ${dbfile} "select sum(nDataLines) from REACODE"`
    echo "  12) database-file: ${dbfile}  date:$FLDATE  size=$FLSIZE"
    echo "      database-data: $updated Entry:$nEntry Datapoints:$nPoints"
}

outExforStat() {
    echo "---EXFOR Statistics---"
	FLSIZE=`ls -lah "${dbfile}" | awk '{print $5}'`
	FLDATE=`date -r ${dbfile} "+%Y-%m-%d,%H:%M:%S"`
	prepared=`sqlite3 ${dbfile} "select max(UpdateDate) from X4UPDATE where UpdateFlag='O'"`
	prepared="${prepared// /,}"
	updated=`sqlite3 ${dbfile} "select max(TransDate) from ENTRY"`
	updated="${updated:0:4}-${updated:4:2}-${updated:6:2}"
	nEntry=`sqlite3 ${dbfile} "select count(*) from ENTRY"`
	nSubent=`sqlite3 ${dbfile} "select count(*) from SUBENT"`
	nDatasets=`sqlite3 ${dbfile} "select count(*) from REACODE where (nDataLines>0)"`
	nPoints=`sqlite3 ${dbfile} "select sum(nDataLines) from REACODE"`
	nWget=`sqlite3 ${dbfile} "select count(*) from wget_cache" 2>/dev/null`
	wget_upd=`sqlite3 ${dbfile} "select max(datim) from wget_cache" 2>/dev/null`
	wget_upd="${wget_upd// /,}"
    echo "  Database-file: ${dbfile}  $FLDATE  size=$FLSIZE"
    echo "  Data in database:"
    echo "  --Database-uploaded: $prepared"
    echo "  --Data-update:       $updated"
    echo "  --Entry/Subent:      $nEntry/$nSubent"
    echo "  --Datasets/points:   $nDatasets/$nPoints"
    if [ "$nWget" != "" ] ; then
	echo "  --wget-cache:        $nWget/$wget_upd"
    fi
    if [ $limitTargets -gt 0 ] ; then
	targHist=`sqlite3 -cmd '.mode table' ${dbfile} "SELECT count(distinct ReacodeID) as Datasets,Target FROM REACSTR where iReacstr=1 group by Target order by Datasets desc limit $limitTargets"`
	echo "  --Datasets by Targets: (limit:$limitTargets)"
	echo "$targHist"|sed 's/^/    /'
    fi
    if [ $limitProjectiles -gt 0 ] ; then
#	projHist=`sqlite3 -cmd '.mode table' ${dbfile} "SELECT count(distinct ReacodeID) as Datasets,Projectile FROM REACSTR where iReacstr=1 group by Projectile order by Datasets desc limit $limitProjectiles"`
	projHist=`sqlite3 -cmd '.mode table' ${dbfile} "SELECT count(distinct ReacodeID) as Datasets,Projectile,Expansion as Help FROM REACSTR left join DICT033 on DICT033.Code=REACSTR.Projectile where iReacstr=1 group by Projectile order by Datasets desc limit $limitProjectiles"`
	echo "  --Datasets by Incident particles: (limit:$limitProjectiles)"
	echo "$projHist"|sed 's/^/    /'
    fi
    if [ $limitReactions -gt 0 ] ; then
	reacHist=`sqlite3 -cmd '.mode table' ${dbfile} "SELECT count(distinct ReacodeID) as Datasets,Reaction FROM REACSTR where iReacstr=1 group by Reaction order by Datasets desc limit $limitReactions"`
	echo "  --Datasets by Reactions: (limit:$limitReactions)"
	echo "$reacHist"|sed 's/^/    /'
    fi
    if [ $limitQuantity -gt 0 ] ; then
#	quanHist=`sqlite3 -cmd '.mode table' ${dbfile} "SELECT count(distinct ReacodeID) as Datasets,Quant,QUANTITY.ShortHelp as Help FROM REACSTR left join QUANTITY on QUANTITY.Code=REACSTR.Quant where iReacstr=1 group by Quant order by Datasets desc limit $limitQuantity"`
	quanHist=`sqlite3 -cmd '.mode table' ${dbfile} "SELECT count(distinct REACSTR.ReacodeID) as Datasets,Quant as Quantity,QUANTITY.ShortHelp as Help FROM REACSTR inner join REACODE on REACODE.ReacodeID=REACSTR.ReacodeID left join QUANTITY on QUANTITY.Code=REACSTR.Quant where iReacstr=1 group by Quant order by Datasets desc limit $limitQuantity"`
	echo "  --Datasets by Quantity: (limit:$limitQuantity)"
	echo "$quanHist"|sed 's/^/    /'
    fi
}

outHelp() {
    cat <<-EOF
	
	----------------------Help----------------------
	Run:
	    $ [bash] x4pro.sh [{options|files}]
	Options:
	   --help  display this text
	Files:
	    file   database file
	Examples:
	    $ bash x4pro.sh
	    $ ./x4pro.sh --help
	    $ bash x4pro.sh quick
	EOF
}

outHelpCommand() {
	echo "---Commands:"
	echo "   A   - run all tests and exit"
	echo "   C   - clean log file, remove generated output files"
	echo "   #   - run example number #, where #:[0..${maxExample}]"
	echo "   #-# - run examples by range of numbers, e.g. 1-5"
	echo "   L   - list examples"
	echo "   S   - statistics of the local EXFOR-database"
	echo "   V   - versions of system components"
#	echo "   H   - type this text"
	echo "   Q   - exit"
}

readExamples() {
#   filenames="*/runme.sh"
    filenames="$1*/runme.sh"
    ii=0
    for name in $filenames; do
	if [ -f $name ]; then
	    ext=${name##*.}
	    dir=$(dirname "${name}")
#	    echo " $ii name:$name dir:$dir ext:$ext"
	    examples[$ii]="$dir"
	    str1=`cat "$dir/content.txt" 2>/dev/null|head -n 1`
	    contents[$ii]="$str1"
#	    echo "---read--- $ii $dir $str1"
	    maxExample=$ii
	    ii=$(($ii+1))
	fi
    done
    nExamples=$ii
}

listExamples() {
    partPrev=""
    for (( ii=0; ii<$nExamples; ii++ )); do
	dir=${examples[$ii]}
	act=${contents[$ii]}
	IFS='-' read -ra array <<< "$dir"
	partNow=${array[0]}
	if [ "$partNow" != "$partPrev" ] ; then
#	    echo "$partNow"
	    partPrev=$partNow
	    arr_plen=${#arr_pdir[@]}
	    for (( ip=0; ip<arr_plen; ip++)); do
#		echo "${arr_pdir[ip]} :: ${arr_ptxt[ip]}"
		prt="${arr_pdir[ip]}"
		txt="${arr_ptxt[ip]}"
#		if [ "$partNow" = "$prt" ] ; then echo "----$partNow---$txt"; fi
#		if [ "$partNow" = "$prt" ] ; then echo -e "----$partNow---\x1b[36m$txt\x1b[0m"; fi
		if [ "$partNow" = "$prt" ] ; then echo -e "    $partNow:: \x1b[36m$txt\x1b[0m"; fi
	    done
	fi
	printf " %-2d %-18s %s\n" $ii "$dir" "$act"
    done
}
clean1() {
	echo "---Clean dirs: remove generated output files."
	if [ "$1" = "" ] ; then
	    read -p "---Are you sure (y/n): " yes
	    yes=$(echo "$yes" | tr '[:upper:]' '[:lower:]')
	    if [ "$yes" != "y" ] ; then return; fi
	fi
	rm -f times.log
	echo -e "\x1b[42;97m--Start  cleaning \x1b[0m"
	echo "---run: ./clean.sh"
	t0=`date +%s`
	./clean.sh
#	source ./clean.sh
	t1=`date +%s`; dt=$(($t1-$t0))
	echo -e "\x1b[45;97m--Finish cleaning \x1b[0m ${dt}sec"
}

runExample1() {
	local nn
	nn=$1
	if [ $nn -gt $maxExample ] ; then
	    echo -e "\e[41;97m---ERROR: example $nn.\e[0m Max:#$maxExample"
	    return
	fi
	DR=${examples[$nn]}
	act=${contents[$nn]}
	printf "%3d) %-44s %s " $nn ${name} `date +%F,%T` >>times.log
	t0=`date +%s`
	pushd "$DR" >/dev/null
#	echo "--example #$nn  $act"
#	printf "\x1b[41;97m--Start  example #%s \x1b[0m %s\n" "$nn" "$act"
#	printf "\x1b[42;97m--Start  example #%s \x1b[0m %s\n" "$nn" "$act"
	printf "\x1b[42;97m--Start  example #%s \x1b[0m \x1b[36m%s\x1b[0m\n" "$nn" "$act" #white on green
#	printf "\x1b[42;30m--Start  example #%s \x1b[0m \x1b[36m%s\x1b[0m\n" "$nn" "$act" #black on green
#	echo "--run: $DR/runme.sh $2 pid:$$"
	echo "---run: $DR/runme.sh $2"
	./runme.sh $2
#	source runme.sh $2
	popd >/dev/null
	t1=`date +%s`; dt=$(($t1-$t0))
	printf ":: %s  t:%ds\n" $(date +%F,%T) $dt>>times.log
#	echo -e "\x1b[45;97m--Finish example #$nn \x1b[0m ${dt}sec"
#	echo -e "\x1b[43;34m--Finish example #$nn \x1b[0m ${dt}sec" #blue on yellow
#	echo -e "\x1b[42;34m--Finish example #$nn \x1b[0m ${dt}sec" #blue on green
	echo -e "\x1b[42;30m--Finish example #$nn \x1b[0m ${dt}sec" #black on green
#	echo -e "\x1b[42;31m--Finish example #$nn \x1b[0m ${dt}sec" #bright-red on green
}

runAllExamples() {
	echo "---RUN ALL $nExamples EXAMPLES---"
	echo -n "Are you sure (Y/n): "; read aaa
#	aaa=$(echo "$aaa" | tr '[:upper:]' '[:lower:]')
	if [ "$aaa" != "Y" ] ; then return; fi
	$mypython3 -B open-webbrowser.py "index.html#part6"
	echo "Script:$0 `date +%F,%T` start" >times.log
	t00=`date +%s`
	for (( ii=0; ii<$nExamples; ii++ )); do
	    runExample1 $ii $1
	done
	echo ""; echo "Script $0 completed."
	t11=`date +%s`; dt=$(($t11-$t00))
	echo "Script:$0 `date +%F,%T` stop" >>times.log
	hhmmss=`printf "%02d:%02d:%02d" $((dt/3600)) $((dt/60%60)) $((dt%60))`
	echo "Elapsed time: ${dt}sec $hhmmss" >>times.log
	echo ""; echo "See file times.log";echo ""
	cat times.log
#	exit
}

main_x4pro() {

    #---starting main program: Welcome, Help+exit
    setPython3
    outWelcome
    if [ "$1" = "--help" ] ; then outHelp; exit; fi
    if [ "$1" = "-help"  ] ; then outHelp; exit; fi
    if [ "$1" = "-h"     ] ; then outHelp; exit; fi
    outPlatform
    outVersions
    readExamples

    #echo -n "Press ENTER to continue..."; read aaa
#    outHelpCommand

    while [ true ] ; do
#	echo -n "Enter command: "
#	printf "\x1b[35mx4pro>\x1b[0m " #magenta
#	printf "\x1b[44;97mx4pro>\x1b[0m "
	printf "\x1b[44;97m${prompt}\x1b[0m "
	read aaa
	aaa=$(echo "$aaa" | tr '[:upper:]' '[:lower:]')
#	if [ "$aaa" = "h" ] ; then
	if [ "$aaa" = "" ] ; then
	    outHelpCommand
	    continue
	fi
	if [ "$aaa" = "q" ] ; then
	    echo "---EXIT---"
	    exit
	fi
	if [ "$aaa" = "l" ] ; then
	    echo "---EXAMPLES---"
	    listExamples
	fi
	if [ "$aaa" = "s" ] ; then	outExforStat;	fi
	if [ "$aaa" = "c" ] ; then	clean1;		fi
#	if [ "$aaa" = "v" ] ; then	outVersions;	fi
	if [ "$aaa" = "v" ] ; then	outWelcome;outPlatform;outVersions;	fi
	if [ "$aaa" = "a" ] ; then
	    runAllExamples $1
	    #exit
	fi

	num="${aaa//[^0-9]/}"
	if [ "$num" != "" ] ; then
	    IFS='-' read -ra array <<< "$aaa"
	    nn0=${array[0]}
	    nn1=${array[1]}
echo "--nn0=[$nn0] --nn1:[$nn1]"
	    if [ "$nn1" = "" ] ; then nn1="$nn0"; fi
	    nn0="${nn0//[^0-9]/}"
	    nn1="${nn1//[^0-9]/}"
	    if [ "$nn0" != "" ] ; then
	    if [ "$nn1" != "" ] ; then
		nn0=$(($nn0))
		nn1=$(($nn1))
		for (( ii=$nn0; ii<=$nn1; ii++ )); do
		    if [ $ii -lt 0           ] ; then continue; fi
		    if [ $ii -gt $maxExample ] ; then continue; fi
		    runExample1 $ii $1
		done
	    fi
	    fi
	fi
    done

}

#echo "BASH_SOURCE[0]=${BASH_SOURCE[0]}"
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_x4pro "$@"
fi
