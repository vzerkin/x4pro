"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 *******************************************************************************
"""

"""
   Program: versions.py ver.2026-02-15
   Author:  V.Zerkin, Vienna, 2023-2026
   Purpose: version of Python and installed packages
"""

ll=12

ii=0; ii+=1
import platform
print('   '+str(ii)+') '+'python:'.ljust(ll)+' ['+platform.python_version()+']')

ii+=1
try:
    import pip
    print('   '+str(ii)+') '+'pip:'.ljust(ll)+' ['+pip.__version__+']')
except Exception as ex:
    print('   -?-pip is not installed.')

ii+=1
try:
    import matplotlib
    print('   '+str(ii)+') '+'matplotlib:'.ljust(ll)+' ['+matplotlib.__version__+']')
except Exception as ex:
    print('   -?-matplotlib is not installed.')

ii+=1
try:
    import plotly
    print('   '+str(ii)+') '+'plotly:'.ljust(ll)+' ['+plotly.__version__+']')
except Exception as ex:
    print('   -?-plotly is not installed.')

ii+=1
try:
    import requests
    print('   '+str(ii)+') '+'requests:'.ljust(ll)+' ['+requests.__version__+']')
except Exception as ex:
    print('   -?-requests is not installed.')

ii+=1
try:
    import pandas
    print('   '+str(ii)+') '+'pandas:'.ljust(ll)+' ['+pandas.__version__+']')
except Exception as ex:
    print('   -?-pandas is not installed.')
    #print('--------Please install pandas:\n\t$ pip install pandas')
#pip3 list --disable-pip-version-check --format=columns|grep '^pandas '|awk '{print $2}'

ii+=1
try:
    import kaleido
    ver='??'
    try:
        ver=kaleido.__version__
    except Exception as ex:
        ver=''
    print('   '+str(ii)+') '+'kaleido:'.ljust(ll)+' OK. '+ver)
#   print('   '+str(ii)+') '+'kaleido:'.ljust(ll)+' ['+kaleido.__version__+']')
except Exception as ex:
    print('   -?-kaleido is not installed.')
    #print('--------Please install kaleido:\n\t $ pip3 install -U kaleido')

ii+=1
try:
    import couchdb
    print('   '+str(ii)+') '+'couchdb:'.ljust(ll)+' ['+couchdb.__version__+']')
except Exception as ex:
    print('   -?-couchdb is not installed.')
