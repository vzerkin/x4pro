#!/bin/bash

# Author:  Viktor Zerkin <v.zerkin@gmail.com>
# Created: February 17, 2026
# License: MIT
# Script:  quick-test.sh, v.2026-02-10
# Run:     $ ./quick-test.sh [# [# [#...]]]
# Example: $ bash quick-test.sh 1 3 5 12

echo -e "   \e[41;97m Welcome to X4Pro-2026 \e[0m"
cat <<EOF
   +-------------------------------------+
   | Run example-1, or selected examples |
   +-------------------------------------+
EOF

CLEAR="\e[0m"
RED="\e[31m"
CYAN="\e[36m"
echo -e "Script: ${RED}$0${CLEAR} starts at `date +%F,%T`"

source x4pro.sh

setPython3
#outWelcome
#outPlatform
#outVersions
readExamples
echo "---Available examples: 0-$maxExample"

declare -a arrExamples=(1)
ii=0; nn=0
for aaa in "$@"; do
#    echo "--param:$aaa"
    num="${aaa//[^0-9]/}"
    if [ "$num" != "" ] ; then
	num=$(($num))
	dir=${examples[$num]}
	act=${contents[$num]}
	echo -e "---example:$aaa $dir ${CYAN}$act${CLEAR}"
	arrExamples[$ii]=$num
	ii=$(($ii+1))
    fi
done

echo "---Running #${#arrExamples[@]} example(s): ${arrExamples[@]}"
read -p "---Are you sure [y]: " yes
yes=$(echo "$yes" | tr '[:upper:]' '[:lower:]')
if [ "$yes" != "n" ] ; then
    len=${#arrExamples[@]}
    for (( ii=0; ii<len; ii++)); do
	nn="${arrExamples[ii]}"
	runExample1 $nn
    done
fi
#echo ""
echo -en "Script: ${RED}$0${CLEAR} completed `date +%F,%T`"
