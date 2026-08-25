#!/bin/bash
cd x4pro1

echo "1. Check whether fortran codes need compilation"
part1-fortran/f00.exe
errCode=$?
echo "---Error-code=$errCode"
if [ $errCode -ne 0 ] ; then #probably this exe is compiled on another OS
	echo "Make sure that you have run ./init-lin.sh"
	echo -n " Run ./init-lin.sh [y] ? "; read aaa
	if [ "$aaa" != "n" ] ; then
            bash init-lin.sh
	    echo -n "Press ENTER to continue... "; read aaa
	fi
fi

echo "2. Check local SQLite EXFOR database"
if [ ! -f "../x4sqlite1.db" ] ; then
    if [ -f "../x4sqlite1.db.zip" ] ; then
	cd ..
	echo -n " unzip x4sqlite1.db.zip [y] ? "; read aaa
	if [ "$aaa" != "n" ] ; then
	    set -x
	    unzip x4sqlite1.db.zip
	    rm -i x4sqlite1.db.zip
	    set +x
	fi
	cd x4pro1
    fi
fi

echo "3. Check dialog and run interactive script for X4Pro"
dialog --version
errCode=$?
if [ $errCode -ne 0 ]; then
    echo "---The package dialog is NOT installed---"
    echo "---Running basic interactive script: x4pro.sh"
    bash x4pro.sh
else
    echo "---The package dialog is installed---"
    echo -n "---Do you want to run menu-based script x4pro2.sh [y] ? "; read aaa
    if [ "$aaa" != "n" ] ; then
	echo "---Running menu-based interactive script: x4pro2.sh"
	bash x4pro2.sh
    else
	echo "---Running basic interactive script: x4pro.sh"
	bash x4pro.sh
    fi
fi
