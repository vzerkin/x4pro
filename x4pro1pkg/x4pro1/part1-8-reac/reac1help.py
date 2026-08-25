"""
 **********************************************************************
 * Copyright (c) 2026 Viktor Zerkin, v.zerkin@gmail.com               *
 * Author:   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026) *
 * License:  MIT License (MIT)                                        *
 **********************************************************************
"""

def getHelp():
    return '''
---------------------------------Help----------------------------------------
Purpose: Retrieve and plot any type EXFOR data from local EXFOR database

Introduction:
  * computational data are presented as function y=f(x1,x2,..)
    where f is measured quantity, xi are independent variables:
     EN  - incident energy
     ANG - angle of outgoing particle
     E2  - energy of outgoing particle
     EVL - energy level
    etc.

Algorithm:
  * user defines EXFOR Reaction-code for data search, x-variable by number
  * selects x-variable by number (default: x1)
  * other variables will be used as parameter for grouping of data points

Usage:
    $ python [{flag}] x4update.py {[option|reaction]}
      * flag: see all Python flags:  $ python --help
        -B         don't write .pyc files on import
      * option:
        -help        print this help-text and exit (also --help)
        -o:<file>    output file name
        -x:x?        set x variable: "x1" to "x5", e.g. -x:x2, default: -x:x1
        -x?fam:<str> filter for "families" of x? variable, e.g. -x2fam:"LVL;EXC"
        -x?min:<num> filter out values of x? variable, e.g. -x1min:6e6
        -x?max:<num> filter out values of x? variable, e.g. -x1max:30e6
        -nogrp       avoid groupping datasets by reaction-codes on the plot
        -fx:<num>    set factor for x-values, e.g. -fx:1e6 sets "MeV" on X-Axis
        -fy:<num>    set factor for y-values, e.g. -fy:1e-3 sets "mb/sr" on Y-Axis
        plotting:
        -xlog           logarithmic scale of X-Axis
        -ylog           logarithmic scale of Y-Axis
        -xmin:<num>     set min of initial x-range of the plot
        -xmax:<num>     set max of initial x-range of the plot
        -lines          connect points on the plot by lines
        -sym            draw border of a symbol of a data point on the plot
        -annot:x,y,txt  annotation on top of the plot;
                        x and y should be given in units of the plot;
                        text can include html tags: <b>, <sup>
      * reaction:    file name should not start with sign "-"
        <reaction>   full EXFOR Reaction-code, e.g. "8-O-16(N,EL)8-O-16,,DA"

Examples.
  1) SIG(Ei) Cross sections
     $ python -B reac1.py "13-AL-27(N,A)11-NA-24,,SIG"

  2) DA(Ei)  Angular distributions
     $ python3 -B reac1.py -o:da1e -x:x1              \\
         -x1max:6.5e6 -x2min:160 -x2max:170           \\
         -lines -sym -ylog -fx:1e3 -fy:1e-3           \\
         -annot:"2500,250,DA(E) <sup>14</sup>N(a,a')" \\
         "7-N-14(A,EL)7-N-14,,DA">da1e.tto

  3) DE(Eo)  Emission spectra
	$ python -B reac1.py -o:de1 -x:x2             \\
            -x1min:6e6 -fx:1e6 -fy:1e-9 -lines -ylog  \\
            "90-TH-232(N,X)0-NN-1,,DE"

  4) DAE(Eo) Double differential cross section
	$ python -B reac1.py -o:de1 -x:x2             \\
            -x1min:6e6 -fx:1e6 -fy:1e-9 -lines -ylog  \\
            "90-TH-232(N,X)0-NN-1,,DE"

  5) TKE(Mass) Total Kinetic Energy
	$ python -B reac1.py -o:tke1 -x:x2            \\
            -fy:1e6 -lines -sym                       \\
            -annot:"80,180,<b>TKE</b>"                \\
            "92-U-235(N,F)MASS,PRE,KE,LF+HF"          \\
            "92-U-235(N,F)MASS,PRE,KE,LF+HF,MXW"

  6) ETA(Ri) Neutron yield (Eta)
	$ python -B reac1.py -o:eta1 -x:x1 -x1max:4   \\
            -lines -sym -ylog                         \\
            -annot:"0.75,3.25,<b>ETA</b>"             \\
            "92-U-235(N,ABS),,ETA">eta1.tto
    '''
