"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 *******************************************************************************
"""

import sys
sys.path.append('./')
sys.path.append('../')
from webdb import *

import requests

api0url='https://nds.iaea.org/exfor'
#api0url='http://localhost:5557/exfor2'
myVerify=True
#web0='https://www-nds.atomstandard.ru/exfor'
#myVerify=False

put2db=True #save to database-cache
get1db=True #get from database-cache before wget

def wget_nds(prog,params,debug=False):
    #print('---wget_nds---')
    txt=None
    txtFromWeb=False
    if get1db:
        txt=wgetdb_get(api0url,prog,params,debug=False)
    if txt is None:
        url=api0url+prog+params
        print('...wget_nds:URL:'+url)
        try:
            url=requests.get(url,verify=myVerify)
        except Exception as ex:
            print("___1___api_wget-error:\n"+str(ex))
            return None
        txt=url.text
        txtFromWeb=True
    if debug:
        print('---wget_nds---txt='+str(txt))
    if put2db and txtFromWeb:
#        print('txt='+txt)
        wgetdb_put(api0url,prog,params,txt,debug=False)
    return txt
