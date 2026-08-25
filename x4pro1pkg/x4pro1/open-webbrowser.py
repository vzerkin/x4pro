"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 *******************************************************************************
"""

import os
import sys
import webbrowser

silent=True

if not silent:
    print("Program: open-webbrowser.py, ver. 2026-02-23")
    print("         by V.Zerkin, Vienna, 2023-2026")
    print("Open Web-Browser with local files and Web URL's")

if (len(sys.argv)<=1):
    print("Example:")
    print("  $ python -B open-webbrowser.py file1.html file2.htm")
    print("  $ python -B open-webbrowser.py part1-1-sig/Al27na-1.htm")
    print("  $ python -B open-webbrowser.py https://nds.iaea.org/cdroms/#x4pro1")
    print("  $ python -B open-webbrowser.py index.html")
    sys.exit(2)

for ii,href in enumerate(sys.argv):
    if (ii>0):
        if (not href.startswith('http')): href='file:///'+os.getcwd()+'/'+href
        print(str(ii)+') Open: ',href)
        webbrowser.open(href, new=2)

if not silent:
    print("Program successfully completed.")
