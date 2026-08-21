@call %~dp0win-bash-gfortran\mingwvars.bat
@call %~dp0win-python3\python3-vars.bat
@call %~dp0sqlite-tools-win\set-env.bat

gfortran --version
python --version
sqlite3 --version
