"""
 *******************************************************************************
 * Copyright: (C) 2024-2025 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2025) *
 *******************************************************************************
"""

import math
import json
import os
import sys
import webbrowser

#_________________Preparing EXFOR data for plot_________________
def prepareExforDataForPlot(datasets,msize=8,groupReac=False,autocolor=False,lines=False,lwidth=0,maxlegend=30
	,lblPrefix=''
	,symBorder=False
	,useRecalcFlag=False
	,bwColor=False
	):
    ldata=len(datasets)
    data1=[]; ii=0; iir=0; lastReacode='?'
    for dataset in datasets:
        flagModif0=''
        flagModif1=''
        msize1=msize
        iSymPlus=0
        symColor='Black'
        symWidth=1
        hiden0=False
        if useRecalcFlag:
            flagModif0='X ' #Original EXFOR data
            symBorder=True
            if dataset['x4lbl'].find('#')>=0:
                flagModif0='R '   #Multiplied:   CS=Ratio*m1
                #flagModif1=':ratio*m1'   #Multiplied:   CS=Ratio*m1
                flagModif1=':'+dataset['x4corr']   #Multiplied:   CS=Ratio*m1
                symBorder=False
                msize1=msize+2
                iSymPlus=100  #-open
            elif dataset['x4lbl'].find('*')>=0:
                flagModif0='A ' #Automatically renormalized: CS=CS/m0*m1 (auto-corrected)
                #flagModif1=':cs/m0*m1' #Renormalized: CS=CS/m0*m1
                flagModif1=':'+dataset['x4corr']   #Renormalized: CS=CS[/m0*m1][*dd][*dm]
                symBorder=True
                symColor='Red'
                msize1=msize+2
                #iSymPlus=200	#-dot
                iSymPlus=300	#-open-dot
                symWidth=1.8
            if dataset.get('x4evalflags') is not None:
                flagModif1+=' flags:'+dataset['x4evalflags']
                if "n" in dataset['x4evalflags']: hiden0=True
        lbl=lblPrefix+str(ii+1)+') '+flagModif0+dataset['x4lbl']+' pt:'+str(len(dataset['x']))\
		+' x4:'+dataset['DatasetID']+flagModif1
        row0=dataset.get('row0')
        if row0 is not None:
            corr_author=row0.get('corr_author')
            if corr_author is not None: lbl='['+corr_author+']: '+lbl
        tr={
	 "text":dataset['x4lbl']
	,"name":lbl
	,"marker_symbol":str((ii%25)+iSymPlus)
	,"marker_size":msize1
	,"mode":"markers"
	}
        if (groupReac):
            if dataset['Reacode']!=lastReacode:
                iir+=1
                lastReacode=dataset['Reacode']
            tr['legendgroup']='exGrp'+str(iir)
            tr['legendgrouptitle.text']=""+dataset['Reacode']
        if hiden0: tr['visible']='legendonly'

        obj1=dataset
        obj1['tr']=tr
        dataset['LIBRARY']='EXFOR'
        dataset['mode']='points'
        data1.append(obj1)
        ii+=1
        print('Plot:'+str(ii)+'/'+str(ldata)+')'+' #'+str(dataset['DatasetID'])+' '+str(dataset['x4lbl'])+' pt:'+str(len(dataset['x'])))
    return data1

#_________________Plot data from EXFOR and ENDF_________________
def myOfflinePlot(data1,ptitle,xtitle,ytitle
    ,xtype='linear',ytype='linear',filename='temp-plot'
    ,flagShow=True
    ,xrange=None
    ,yrange=None
    ,legendInside=True
    ,how2plot=1
    ,xstep30=False
    ,annot1=None
    ,plotParams=None
    ):

    if not filename.endswith('.html'): filename=filename+'.html'


    obj1={}
    obj1['data1']=data1
    ff=open(filename,'w')
    ff.write('''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>X4Pro-MyPlot</title>

<script src="../../jsx/plotly-2.min.js"></script>
<link rel="stylesheet" href="../../x4js/x4pro2.css">
<script src="../../x4js/zvSwitch.js"></script>
<script src="../../x4js/gg.js"></script>
<script src="../../x4js/ggp.js"></script>
<script src="../../x4js/ggpd.js"></script>
<script src="../../x4js/ggx.js"></script>
<script src="../../x4js/ggsub.js"></script>
<script src="../../x4js/x4pro2pro.js"></script>

<script src="../jsx/plotly-2.min.js"></script>
<link rel="stylesheet" href="../x4js/x4pro2.css">
<script src="../x4js/zvSwitch.js"></script>
<script src="../x4js/gg.js"></script>
<script src="../x4js/ggp.js"></script>
<script src="../x4js/ggpd.js"></script>
<script src="../x4js/ggx.js"></script>
<script src="../x4js/ggsub.js"></script>
<script src="../x4js/x4pro2pro.js"></script>

</head>
<body bgcolor=#f0f0ff onload="javascript:bodyOnload();">
<script language="javascript">
''')

    if plotParams is not None:
        ff.write('plotParams=\n')
        json.dump(plotParams,ff,indent=2)
        ff.write(';\n')

    ff.write('data4plot=\n')
#    json.dump(obj1,ff,indent=2)
    json.dump(data1,ff,indent=2)
    ff.write(';\n')

    ff.write('''    x4pro_outAll(data4plot);
</script>
</body>
</html>
''')

    href='file:///'+os.getcwd()+'/'+filename
    print('Open Page: ',href)
    webbrowser.open(href, new=2)

    return
