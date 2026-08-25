#!/bin/bash
echo "________Make program executables *.exe on Windows"
echo "________Your gfortran version:"
gfortran --version
set -x

gfortran f00.f -o f00.exe -static
gfortran f1.f       sql1sub.c sqlite3.c -o f1.exe       -static
gfortran dae1e2.f   sql1sub.c sqlite3.c -o dae1e2.exe   -static
gfortran sig1.f     sql1sub.c sqlite3.c -o sig1.exe     -static
gfortran sig1toc4.f sql1sub.c sqlite3.c -o sig1toc4.exe -static
gfortran legrs2da.f sql1sub.c sqlite3.c -o legrs2da.exe -static

echo "________Result: file f1.exe dae1e2.exe sig1.exe sig1toc4.exe legrs2da.exe"
ls -la f1.exe dae1e2.exe sig1.exe sig1toc4.exe legrs2da.exe
