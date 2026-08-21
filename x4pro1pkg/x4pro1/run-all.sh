#!/bin/bash
#set -x

# Author:  Viktor Zerkin <v.zerkin@gmail.com>
# Created: February 17, 2026
# License: MIT

# Script:  run-all.sh, v.2026-02-20
# Run:     $ run-all.sh [pattern]
# Example: $ bash run-all.sh part1
#          $ bash run-all.sh "*sig"
#          $ bash run-all.sh "*leg"

echo -e "   \e[41;97m Welcome to X4Pro-2026 \e[0m"
cat <<EOF
   +---------------------------------------+
   | Run all examples, or part of examples |
   +---------------------------------------+
EOF

#---Text settings.
CLEAR="\e[0m"
CYAN="\e[36m"
echo -e "Script: ${CYAN}$0${CLEAR} starts at `date +%F,%T`"

source x4pro.sh

setPython3
#outWelcome
#outPlatform
#outVersions
readExamples "$@"
listExamples

#runAllExamples "$@"
runAllExamples

echo -en "Script: ${CYAN}$0${CLEAR} completed `date +%F,%T`"
