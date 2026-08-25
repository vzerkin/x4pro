"""
 *******************************************************************************
 * Copyright: (C) 2023-2025 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2025) *
 *******************************************************************************
"""

import json

def prepareEndfDataForPlot(datasets,legendgroup,dy_showlegend,autocolor=False,lwidth=4,showAuth=False):
    ldata=len(datasets)
    ii=0; data1=[]
    for dataset in datasets:
        name=str(ii+1)+') '+dataset['x4lbl']
        tr={
	 "text":dataset['x4lbl']
	,"name":name
	,"color":dataset['myColor']
	,"width":lwidth
	,"mode":"lines"
	}
        if (legendgroup!=''):
            tr['legendgroup']=legendgroup
            tr['legendgrouptitle.text']="EVALUATED DATA"

        obj1=dataset
        obj1['tr']=tr
        dataset['LIBRARY']=dataset['x4lbl']
        dataset['mode']='curve'

        data1.append(obj1)
        ii+=1
        print('Plot:'+str(ii)+'/'+str(ldata)+') '+str(dataset['DatasetID'])+'\t'+str(dataset['x4lbl'])+'\tpt:'+str(len(dataset['x']))+'\tcolor:'+dataset['myColor'])

    return data1
