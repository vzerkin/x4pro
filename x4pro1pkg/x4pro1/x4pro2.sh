#!/bin/bash
#set -x

# Author:  Viktor Zerkin <v.zerkin@gmail.com>
# Created: February 19, 2026
# License: MIT

dia_pause1() {
    read -rsp $'\nPress any key to continue...' -n1 key
}

dia_selectCategory() {
    local LST=()
    local i3=0
    local arr_plen=${#arr_pdir[@]}
    for (( ip=0; ip<arr_plen; ip++)); do
#	echo "${arr_pdir[ip]} :: ${arr_ptxt[ip]}"
	prt="${arr_pdir[ip]}"
	nn=`ls -1 ${prt}*/runme.sh 2>/dev/null|wc -l`
	if [ $nn -le 0 ]; then continue; fi
	pp=${prt//part/}
	txt="${arr_ptxt[ip]}"
	LST[$i3]="$pp"; i3=$(($i3+1))
	LST[$i3]="part-$pp $txt"; i3=$(($i3+1))
    done
#    echo "${#LST[@]}---LST:${LST[@]}"
#echo -n "pause..."; read qqq

    local lmenu=${#LST[@]}
    local lmenu=$(($lmenu /2 ))
    local HH=$(($lmenu +6))
#   CHOICE2=$(dialog --clear \
    CHOICE2=$(dialog \
            --backtitle "$BACKTITLE" \
            --title " Select Category " \
	    --menu "" $HH 80 $lmenu "${LST[@]}" \
            2>&1 >/dev/tty)
    echo "---CHOICE2=${CHOICE2}"
    if [ "${CHOICE2}" = "" ]; then return; fi
    dia_selectFromCategory "${CHOICE2}"
    dia_pause1
}

dia_selectFromCategory() {
    local p="part$1"
    local LST=()
    local NUMEX=()
    local i3=0
    local i2=0
    local ii
    local ptxt=""
    local arr_plen=${#arr_pdir[@]}
    for (( ip=0; ip<arr_plen; ip++)); do
#	echo "${arr_pdir[ip]} :: ${arr_ptxt[ip]}"
	prt="${arr_pdir[ip]}"
	txt="${arr_ptxt[ip]}"
	if [ "$prt" != "$p" ] ; then continue; fi
	ptxt="$txt"
    done

    for (( ii=0; ii<$nExamples; ii++ )); do
	dir=${examples[$ii]}
	act=${contents[$ii]}
	IFS='-' read -ra array <<< "$dir"
	partNow=${array[0]}
#echo "---dia_selectFromCategory--ii:$ii dir:$dir partNow:$partNow p:$p"
	if [ "$partNow" != "$p" ] ; then continue; fi
	NUMEX[$i2]="$ii"
#	LST[$i3]="$ii"; i3=$(($i3+1))
	LST[$i3]="$i2"; i3=$(($i3+1)); i2=$(($i2+1))
#	LST[$i3]="$dir/ $act"; i3=$(($i3+1))
#	LST[$i3]=`printf "%-18s %s" "$dir" "$act"`; i3=$(($i3+1))
	LST[$i3]=`printf "%-2d %-18s %s" "$ii" "$dir" "$act"`; i3=$(($i3+1))
	LST[$i3]="on";  i3=$(($i3+1))
    done
#    echo "${#LST[@]}---LST:${LST[@]}"
#    CHOICE3=$(dialog --keep-window \
    CHOICE3=$(dialog --keep-tite \
            --backtitle "X4Pro" \
            --title " Select examples and run " \
	    --checklist "$ptxt" 15 88 15 "${LST[@]}" \
                    2>&1 >/dev/tty)
    echo "---CHOICE3=${CHOICE3}"
    CHOICE3=${CHOICE3//\"/}; CHOICE3=" $CHOICE3 " #needed for Linux
    echo "---CHOICE3=[${CHOICE3}]"

    echo "${#NUMEX[@]}---NUMEX:${NUMEX[@]}"
    local len=${#NUMEX[@]}
    local num
    for (( ii=0; ii<len; ii++)); do
	num=${NUMEX[ii]}
	substr=" $ii "
	if [[ "${CHOICE3}" == *"$substr"* ]]; then
	    echo "---It's there! CHOICE3:[${CHOICE3}] ii:$ii substr:$substr num:$num"
	    runExample1 $num
	fi
    done
}

dia_runChoice() {
    IFS=' ' read -ra array <<< "$1"
    local len=${#array[@]}
    local num
    local ii
    for (( ii=0; ii<len; ii++)); do
	num=${array[ii]}
	num=${num//\"/}
	num="${num//[^0-9]/}"
	echo "---dia_runChoice---num:$num"
	runExample1 $num
    done
}

dia_listAndRun() {
    local LST=()
    local i3=0
    local sym
    for (( ii=0; ii<$nExamples; ii++ )); do
#    for (( ii=0; ii<3; ii++ )); do
	dir=${examples[$ii]}
	act=${contents[$ii]}
#	LST[$i3]="$ii"; i3=$(($i3+1))
	sym="$ii"
	if [ $ii -ge 10 ] ; then
	    isym=$(($ii-10+65))
	    isym=$(($ii-10+97))
	    sym=`echo "$isym" | awk '{printf("%c",$1)}'`
	    sym="$sym$ii"
#	    sym="$sym$(($ii%10))"
	fi
#	dir=${dir//part/}
	LST[$i3]="$sym"; i3=$(($i3+1))
#	LST[$i3]="$dir/ $act"; i3=$(($i3+1))
	LST[$i3]=`printf "%-18s %s" "$dir" "$act"`; i3=$(($i3+1))
#	LST[$i3]=`printf "%-2d %-18s %s" "$ii" "$dir" "$act"`; i3=$(($i3+1))
	LST[$i3]="$1";  i3=$(($i3+1))
    done
#tst    echo "${#LST[@]}---LST:${LST[@]}"
#tst    dia_pause1
#    CHOICE2=$(dialog --clear \
    CHOICE2=$(dialog --keep-window \
            --backtitle "$BACKTITLE" \
            --title " Run selected examples " \
	    --checklist "" 33 100 33 "${LST[@]}" \
	2>&1 >/dev/tty)
    echo "---CHOICE2=${CHOICE2}"
    if [ "${CHOICE2}" = "" ]; then return; fi
    dia_runChoice "${CHOICE2}"
    dia_pause1
}

main_x4pro_dia() {
    #---starting main program: Welcome, Help+exit
    setPython3
    outWelcome
    if [ "$1" = "--help" ] ; then outHelp; exit; fi
    if [ "$1" = "-help"  ] ; then outHelp; exit; fi
    if [ "$1" = "-h"     ] ; then outHelp; exit; fi
#    outPlatform
#    outVersions
    readExamples

    OPTIONS=(
	"A" "Run all examples"
	"L" "List, select and run examples"
	"P" "Select category/part and run examples"
	"C" "Clean: remove generated output files"
	"S" "Statistics of the local EXFOR-database"
	"V" "Versions of system components"
	"Q" "Exit"
	)

    lmenu=${#OPTIONS[@]}
    lmenu=$(($lmenu /2 ))

    HEIGHT=13
    HEIGHT=$(($lmenu +6))
    WIDTH=51
    CHOICE_HEIGHT=$lmenu
    BACKTITLE="X4Pro-dialog"
    TITLE=" Main menu "
    #MENU="Select command:"
    MENU=""
    default="L"


    while true; do
#	CHOICE=$(dialog --clear \
#	CHOICE=$(dialog \
	CHOICE=$(dialog --keep-window \
	            --backtitle "$BACKTITLE" \
	            --title "$TITLE" \
--default-item "$default" \
                  --menu "$MENU" \
                    $HEIGHT $WIDTH $CHOICE_HEIGHT \
	            "${OPTIONS[@]}" \
                    2>&1 >/dev/tty)
#--begin 4 12
#--no-cancel
#--no-kill
#	echo "---CHOICE=$CHOICE"
	default="L"
	case $CHOICE in
	A)
#	    echo "----------A---------"
	    dia_listAndRun on
            ;;
	P)
#	    echo "----------P---------"
	    default="$CHOICE"
	    dia_selectCategory
#	    dia_pause1
            ;;
	L)
#	    echo "----------L---------"
	    dia_listAndRun off
            ;;
	C)
	    dialog --title "Cleaning directories" --defaultno --yesno "Are you sure?" 5 25
	    if [ $? -eq 0 ]; then
		clean1 "dia"
		dia_pause1
	    fi
            ;;
	V)
	    outWelcome
	    outPlatform
	    outVersions
	    dia_pause1
            ;;
	S)
	    outExforStat
	    dia_pause1
            ;;
        "Q")
            echo "Good bye!"
            break
            ;;
        "")
            echo "Bye!"
            break
	    ;;
	esac
    done
}

source x4pro.sh

#echo "BASH_SOURCE[0]=${BASH_SOURCE[0]}"
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_x4pro_dia "$@"
fi
