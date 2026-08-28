                      Nuclear Data Section (NDS)
             Department of Nuclear Sciences and Applications
                International Atomic Energy Agency (IAEA)
                Vienna International Centre, P.O. Box 100,
                        A-1400 Vienna, Austria
                Tel:(+43 1) 2600-21714; Fax:(+43 1) 26007
  
        WORKING MATERIALS ON THE DEVELOPMENT OF X4PRO DISTRIBUTION
  
          "X4Pro - universal, fully relational EXFOR database"
             Prepared by Viktor Zerkin, IAEA-NRDC, 2021-2026
            Experimental version for MS-Windows, Linux, MacOS
                 Last modified: 2026-08-28 by V.Zerkin
_______________________________________________________________________________
CONTENT

 1) x4sqlite1.db (SQLite): relational database X4Pro-mini*
    *Mini-version of the database is incomplete. Full version is also available.
 2) x4pro1: directory with set of python3 and gfortan demo programs to retrieve
    and modify EXFOR data and plot them together with evaluated data retrieved
    from ENDF Web system on http://nds.iaea.org/endf
 3) MS-Windows system components*:
    3.a) GNU Fortran (Rev8, Built by MSYS2 project) 15.2.0
    3.b) Python-3.12.5 with installed packages: plotly-6.7.0, matplotlib-3.10.9,
         requests-2.32.3, pandas-2.2.2, kaleido-1.3.0
    3.c) sqlite3: 3.47.2 2024-12-07
    3.d) dialog:  1.1-20100119 2010-04-11
	 download dialog.exe 
	 from:	https://andrear.altervista.org/home/cdialog.php
	 to:	msys\1.0\bin\dialog.exe
    *Note. Provided to avoid any installation on MS-Windows
	   Otherwise, install MinGW-64 from https://www.msys2.org/
	   see details in the file "howto-mingw64.txt"
_______________________________________________________________________________
LICENSES

 1) See LICENSE.TXT
 2) For third party software, please see the README, "license.terms" files that 
    come in the associated directories.
_______________________________________________________________________________
DOWNLOAD

 1) Clone x4pro from GutHub:
    $ git clone https://github.com/vzerkin/x4pro.git
 ~or~
 2) Start Web-Browser, go to URL:
    https://github.com/vzerkin/x4pro
    click "<>Code" and  "Download-ZIP"
 ~or~
 3) Download file "x4pro1-20260828-mini.zip" from Internet:
    https://nds.iaea.org/cdroms/x4pro.htm#x4pro1
_______________________________________________________________________________
UNCOMPRESS

 1) Uncompress file "x4pro1-20260828-mini.zip" (~8Gb)
    or x4pro-master.zip downloaded from GitHub:
    $ unzip ~/Downloads/x4pro-master.zip
    (required free space on HD disk: ~2Gb)
_______________________________________________________________________________
INSTALL

 Windows*:
 1) start Explorer and create icon for "run-x4pro.bat": 
    right-click on the file run-x4pro.bat and select "Send to: Desktop"
 2) start Explorer and create icon "start-x4pro.bat": 
    right-click on the file start-x4pro.bat and select "Send to: Desktop"
 *Note. Windows distibution is portable (having embedded python3, mingw, gfortran)

 Linux/MacOS:
 1) If you downloaded and uncompressed "x4pro1-20260828-mini.zip"
    you can remove preinstalled Windows' system components:
      $ rm -rf x4pro1pkg/win-*
 2) check python3* (install if you don't have it)
      $ python3 --version
    *Note: scripts runme.sh run python codes using command
      ${mypython3} -B <program>.py
      in order to define variable ${mypython3} they call ../mypython3.sh
      where ${mypython3} is set depending of OS:
       --MacOS:   python3
       --Linux:   python3
       --Windows: python
     If you wish to use your own definition, please, modify "mypython3.sh"
 3) install needed pip3 and python3 packages:
      $ sudo apt-get install python3-pip
      $ pip3 install plotly
      $ pip3 install -U kaleido
      $ pip3 install requests
      $ pip3 install matplotlib
      ~or~
      $ python3 -m pip install matplotlib
       *Note. You may need to install another version of matplotlib:
      $ pip3 install matplotlib 'matplotlib==3.6.2'
       *Note. If pip3 install fails with error-message:
        "connection error: [SSL: CERTIFICATE_VERIFY_FAILED]..."
      $ pip3 install --trusted-host files.pythonhosted.org \
        --trusted-host pypi.org --trusted-host pypi.python.org 'plotly>=4.0.0'
      $ pip3 install couchdb
       *Package "couchdb" is optional (details in "part4-0-couchdb/howto.txt")
 4) install and check gfortran
      $ sudo apt-get install gfortran #---Linux
      $ brew install gfortran         #---MacOS
      $ gfortran --version
 5) install and check sqlite3
      $ sudo apt-get install sqlite3  #---Linux
      $ brew install sqlite3          #---MacOS
      $ sqlite3 --version
 6) install and check dialog
      $ sudo apt-get install dialog   #---Linux
      $ brew install dialog           #---MacOS
      $ dialog --version
 7) make fortran executables
      $ cd x4pro1pkg/x4pro1
      $ ./init-lin.sh
 8) Distribution-2026 includes script "run-x4pro.sh" allowing to avoid item 7)
      $ cd x4pro1pkg
      $ ./run-x4pro.sh
_______________________________________________________________________________
STARTUP

 Windows:
 0) Run script to check installation and start interactive tools
	$ cd x4pro1pkg/
	$ run-x4pro.bat
 1) Run all demo-examples:
    double click on the icon "run-x4pro.bat - short-cut"
    or run Explorer and double-click on the file "run-x4pro.bat"
 2) Start using package. Set environment and continue working:
    click on the icon "start-x4pro.bat - short-cut"
    or run Explorer and double-click on the file "start-x4pro.bat"
 ...you should have opened cmd - terminal window
    2a) Quick demo test
        x4pro1> bash quick-test.sh
        ...script will run one test and open Html file in your Web browser...
    2b) Start all demos (or go to selected dir and start individual demo-program)
        x4pro1> bash run-all.sh
        ...script will run all tests and open Html files in your Web browser...
        ...the total running time should be approximately 5-7 minutes....
    2c) Run single example, e.g. script sig1x.py from test-10 in part2-1-sig1/
        x4pro1> cd part2-1-sig1
        part2-1-sig1> python -B sig1x.py "Al-27" "n,a" log lin
 3) Using TUI interactive scripts (TUI: Text-based User Interface)
    3a) Basic interactive script
        x4pro1> bash x4pro.sh
                ...perform operations using keyboard...
    3b) Menu-type interactive script based on "dialog" package
        --------Check whether you have program dialog installed in your MinGW:
        x4pro1> dialog --version
                Version: 1.1-20100119
        --------Start TUI-based script: x4pro2.sh
        x4pro1> bash x4pro2.sh
                ...perform operations...

 Linux/MacOS:
 0) Run script to check installation ans start interactive tools
	$ cd x4pro1pkg/
	$ bash run-x4pro.sh
 1) cd x4pro1pkg/x4pro1
 2) Quick demo test
        $ bash quick-test.sh
        ...script will run one test and open Html file in your Web browser...
 3) Start all demos (or go to selected dir and start individual demo-program)
        $ bash run-all.sh
        $ ./run-all.sh
        ...programs run one after another and open Html files in your Web browser...
        ...the total running time should be approximately 2-3 minutes...
 4) Using interactive scripts
    4a) Basic interactive script
        $ bash x4pro.sh
        ...perform operations using keyboard...
    4b) Interactive script based on "dialog" package with Menu
        #--------Check whether you have program dialog installed in your MinGW:
        $ dialog --version
        Version: 1.3-20211214
        #--------Start TUI-based script: x4pro2.sh
        $ bash x4pro2.sh
        ...perform operations...
_______________________________________________________________________________
SWITCH OUTPUT

 Most of the scripts can be switched from using Plotly to Matplotlib and back.

 Windows:
 1) Set Plotly
    x4pro1> bash set1.sh
 2) Set Matplotlib
    x4pro1> bash set2.sh

 Linux/MacOS:
 1) Set Plotly
    $ ./set1.sh
 2) Set Matplotlib
    $ ./set2.sh
_______________________________________________________________________________

Please report setup/runtime errors to v.zerkin@gmail.com
_______________________________________________________________________________

         ALL PRODUCTS ON THIS PACKAGE ARE PROVIDED IN GOOD FAITH AND 
                    WITHOUT A WARRANTY OF ANY KIND.
