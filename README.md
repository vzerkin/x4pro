# X4Pro - universal, fully relational EXFOR database.<br>Professional edition.
by V.Zerkin, 2026-09-04

## Content

- Documentation
    - general description [index.html](x4pro1pkg/x4pro1/doc/index.html.pdf)
    - examples of plots using [plotly](x4pro1pkg/x4pro1/doc/out2plotly.html.pdf) and [matplotlib](x4pro1pkg/x4pro1/doc/out2matplotlib.html.pdf)
    - News-2026: [description and plots](x4pro1pkg/x4pro1/doc/news2026.html.pdf)
- Database
    - X4Pro/SQLite database: mini-version
- Fortran/C/SQL EXFOR data retrieval demo programs
  - execute SQL and retrieve from local X4Pro: F1, SIG, DAE, SIG&rarr;C4
  - retrieve and recalculate EXFOR data [DA,LEG/RS]&[SIG]&rarr;[DA]&rarr;[C4]
- Python demo codes
    - retrieve/plot local EXFOR data: SIG, DA, DAP, DE, DAE, FY, [CSP](x4pro1pkg/x4pro1/part1-8-reac/out00/sig1p.html.png "partial cross section"), [CST](x4pro1pkg/x4pro1/part1-8-reac/out00/cst1.html.png  "temperature dependent cross section"), [TKE](x4pro1pkg/x4pro1/part1-8-reac/out00/tke1.html.png  "total kinetic energy of primary fission fragments"), [ETA](x4pro1pkg/x4pro1/part1-8-reac/out00/eta1.html.png  "average neutron yield per nonelastic event"), [Nubar](x4pro1pkg/x4pro1/part1-8-reac/out00/nu1.html.png "average number of neutrons per fission"), [Author1](x4pro1pkg/x4pro1/part1-8-reac/out00/Kokkoris.html.png "search by 1st author and data type"), [Product](x4pro1pkg/x4pro1/part1-8-reac/out00/sig1prod.html.png "Production cross section, where product coded as SF4 or in DATA (ELEM/MASS)")
    - retrieve/plot local EXROR and remote ENDF data, e.g. [DA:mf4/34](x4pro1pkg/x4pro1/part2-2-da1an/out00/da1an.html.png), [FY(E)](x4pro1pkg/x4pro1/part2-7-fye/out00/u235-nf-cd115g-cumFY.html.png), [CSP:mt51](x4pro1pkg/x4pro1/part2-8-sig1par/out00/Li7ninl.html.png), [Nubar:mt455](x4pro1pkg/x4pro1/part2-9-nubar/out00/U238nf_dl-nu.html.png), [Eta](x4pro1pkg/x4pro1/part2-A-eta/out00/U235-eta.html.png "Average neutron yield per nonelastic event"), PFNS
    - renormalize and correct EXFOR data: automatically, by own user's code, by expert's codes  
    - recalculate EXFOR data: [Ratio]&rarr;[SIG], [DA,LEG]&rarr;[SIG]
    - recalculate EXFOR data: [DA,LEG/RS]&[SIG]&rarr;[DA]; [DA,LEG]&rarr;[DA]&rarr;[R33]
    - retrieve and plot covariance data coded in EXFOR:	[En&times;En](x4pro1pkg/x4pro1/part1-7-covar/out00/covar1.png), [Reac&times;Reac](x4pro1pkg/x4pro1/part1-7-covar/out00/covar2.png)
    - export X5json from X4Pro to CouchDB (NoSQL database)
    - retrieve CS, ratios, monit-data; renormalize to new standards and decay data; convert ratios to CS: [Zn64np](x4pro1pkg/x4pro1/part6-1-eval2sig/out00/Zn64np.html.png)
- SQL demo commands
    - find zero values of PARITY, ERR-T and DATA-ERR (for EXFOR compilers)
    - generate summary tables with evaluators' flags and scores (for evaluators)
- Bash scripts to observe database and run demo-codes
    - CLI - Command Line Interface for running demo-codes: [x4pro.sh](x4pro1pkg/x4pro1/x4pro.sh)
    - TUI - Text-based User Interface: [simple](x4pro1pkg/x4pro1/doc/x4pro-tui.pdf) and [menu-type](x4pro1pkg/x4pro1/doc/x4pro-dia.pdf)
- System environment (see [readme.txt](x4pro1pkg/readme.txt))
    - Operating Systems: Linux/MacOS/Windows:MinGW
    - Python3 with packages: plotly, matplotlib, requests, etc.
    - gfortran, gcc
    - sqlite3, dialog

## Links

* [NRDC](https://nds.iaea.org/nrdc/) International Network of Nuclear Reaction Data Centres 
* [IAEA-NDS](https://nds.iaea.org/) International Atomic Energy Agency, Nuclear Data Service 
* [EXFOR](https://nds.iaea.org/exfor/) IAEA-NDS Web-Retrieval System 
* [X4Pro](https://nds.iaea.org/cdroms/#x4pro1) Download previous versions of the package from IAEA-NDS site
* ND2022 - Nuclear-Data Conference: X4Pro [reference paper](https://doi.org/10.1051/epjconf/202328414015), [presentation](https://indico.frib.msu.edu/event/52/contributions/875/attachments/487/2289/nd2022-zerkin1.pdf)
