"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import sys
sys.path.append('./')
from myCorr1 import *

myFuncs={
	 '142710031':fcorr_142710031
	,'41455005' :fcorr_41455005
}

def corr_dataset(rows,cursor):
    newrows=[]
    if len(rows)<=0: return newrows
    row=rows[0]
    DatasetID=row['DatasetID']
    print("___________corr_dataset:::["+DatasetID+']'+' len='+str(len(rows)))
    myFunc=myFuncs.get(DatasetID)
    if myFunc is None: return newrows
    for row in rows:
        #print(row)
        iupd=myFunc(row)
        if iupd>0:
            newrows.append(row);
            row['corrected']=1
    return newrows
