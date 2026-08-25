"""
 *********************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)            *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                       *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA (1999-2023), NRDC (1996-2026) *
 *********************************************************************************
"""

import math
import matplotlib.pyplot as plt

def prepareErrorArray(array,ll):
    if array is None: return [0*ll]
    err=[]
    for err1 in array:
        if err1 is None: err1=0
        err.append(err1)
    return err

#_________________Preparing EXFOR data for plot_________________
def prepareExforDataForPlot(datasets,msize=8,groupReac=False,lines=False,lwidth=0,maxlegend=30
	,lblPrefix=''
	,symBorder=False
	,useRecalcFlag=False
	):
    ldata=len(datasets)
    #https://matplotlib.org/stable/api/markers_api.html
    markers=['o','s','D','P','X','^','v','<','>','*','x','+']
    data1=[]; ii=0
    for dataset in datasets:
        #if (len(dataset['x'])<=1): continue
        #plt.scatter(dataset['x'],dataset['y'], s=60, c='red', marker='^')
        dy=prepareErrorArray(dataset.get('dy'),len(dataset['x']));
        dx=prepareErrorArray(dataset.get('dx'),len(dataset['x']))
        mrk=markers[ii%len(markers)]
        mfc=None
        if lblPrefix!='': mfc='none'
        flagModif0=''
        flagModif1=''
        hiden0=False
        if useRecalcFlag:
            flagModif0='X ' #Original EXFOR data
            if dataset['x4lbl'].find('#')>=0:
                flagModif0='R '   #Multiplied:   CS=Ratio*m1
                flagModif1=':ratio*m1'   #Multiplied:   CS=Ratio*m1
                flagModif1=':'+dataset['x4corr']   #Multiplied:   CS=Ratio*m1
            elif dataset['x4lbl'].find('*')>=0:
                flagModif0='A ' #Automatically renormalized: CS=CS/m0*m1 (auto-corrected)
                #flagModif1=':cs/m0*m1' #Renormalized: CS=CS/m0*m1
                flagModif1=':'+dataset['x4corr']   #Renormalized: CS=CS[/m0*m1][*dd][*dm]
            if dataset.get('x4evalflags') is not None:
                flagModif1+=' flags:'+dataset['x4evalflags']
                if "n" in dataset['x4evalflags']: hiden0=True
        lbl=lblPrefix+str(ii+1)+') '+flagModif0+dataset['x4lbl']+' pt:'+str(len(dataset['x']))\
		+' x4:'+dataset['DatasetID']+flagModif1
#		+' #'+dataset['DatasetID']+flagModif1
        row0=dataset.get('row0')
        if row0 is not None:
            corr_author=row0.get('corr_author')
            if corr_author is not None: lbl='['+corr_author+']: '+lbl
        if dataset.get('DatasetSplit') is not None: lbl+=' '+dataset['DatasetSplit']
        if (ii>=maxlegend): lbl=None
        plt.errorbar(dataset['x'],dataset['y']
#	        ,yerr=[dy,dy],xerr=[dx,dx],elinewidth=0.4,capsize=2,capthick=0.4
	        ,yerr=[dy,dy],xerr=[dx,dx],elinewidth=0.7,capsize=2,capthick=0.4
		,markersize=msize/1.55, marker=mrk
#		,mfc=mfc
		,linestyle='-',linewidth=lwidth
		,label=lbl
		,alpha=0.8
		,zorder=1.5
	)
        ii+=1
        print('Plot:'+str(ii)+'/'+str(ldata)+')'+' #'+str(dataset['DatasetID'])+' '+str(dataset['x4lbl'])+' pt:'+str(len(dataset['x'])))
        #if (ii>=30): break
    return data1

#_________________Plot data from EXFOR and ENDF_________________
def myOfflinePlot(data1,ptitle,xtitle,ytitle
    ,xtype='linear',ytype='linear',filename='temp-plot'
    ,flagShow=False
    ,xrange=None
    ,yrange=None
    ,legendInside=True
    ,how2plot=1
    ,xstep30=False
    ,annot1=None
    ,plotParams=None
    ):

    filename=filename.replace('.html','').replace('.htm','')
    ptitle=ptitle.replace('<br>','\n').replace('<i>','').replace('</i>','').replace('<b>','').replace('</b>','')
#    plt.title('Matplotlib: '+ptitle)
    plt.title(ptitle)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.xscale(xtype)
    plt.yscale(ytype)

    if legendInside:
#        plt.gcf().set_size_inches(9,7)
        plt.gcf().set_size_inches(9.6,7)
        legend=plt.legend()
        #legend=plt.legend(facecolor="white",framealpha=1)
    else:
#        plt.gcf().set_size_inches(14,9)
#        plt.gcf().set_size_inches(12,7)
#        plt.gcf().set_size_inches(12.8,7)
#        plt.gcf().set_size_inches(13.4,7)
        plt.gcf().set_size_inches(14.4,8.5)
#        plt.subplots_adjust(left=0.06,right=0.7)
#        plt.subplots_adjust(left=0.06,right=0.64)
        plt.subplots_adjust(left=0.074,right=0.64)
#        legend=plt.legend(facecolor="white",framealpha=1,bbox_to_anchor=(1,0.8),prop={'family':'Arial','size':9})
#        legend=plt.legend(facecolor="white",framealpha=1,bbox_to_anchor=(1,1.01),prop={'family':'Arial','size':9})
        legend=plt.legend(facecolor="white",framealpha=1,bbox_to_anchor=(1,1.01),prop={'family':'Arial','size':7})

    if xrange is not None: plt.xlim(xrange[0],xrange[1])
    if yrange is not None: plt.ylim(yrange[0],yrange[1])

    #plt.tight_layout(rect=[0,0,1.2,1])
#    plt.grid(b=True, which='major')
#    plt.grid(b=True, which='minor', linewidth=0.2)
    plt.grid(True, which='major')
    plt.grid(True, which='minor', linewidth=0.2)
    if xstep30: plt.xticks(range(0,181,30)) #display xticks with step 30
    #plt.minorticks_on()
    plt.savefig(filename+'.png')
    plt.savefig(filename+'.pdf')
    if flagShow:
        print('\nPress Q to exit...')
        plt.show()
