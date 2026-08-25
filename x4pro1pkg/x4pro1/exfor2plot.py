"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 *******************************************************************************
"""

import sys
import math
import plotly
from plotly.graph_objs import Scatter,Layout
import plotly.graph_objects as go

#_________________Preparing EXFOR data for plot_________________
def prepareExforDataForPlot(datasets,msize=8,groupReac=False,autocolor=False,lines=False,lwidth=0,maxlegend=30
	,lblPrefix=''
	,symBorder=False
	,useRecalcFlag=False
	):
    ldata=len(datasets)
    symBorder0=symBorder
    data1=[]; ii=0; iir=0; lastReacode='?'
    for dataset in datasets:
        #if (len(dataset['x'])<=1): continue
        #error_y=dict(type='data',array=dataset['dy'],visible=True,thickness=0.7)
        #error_x=dict(type='data',array=dataset['dx'],visible=True,thickness=0.9)
        symBorder=symBorder0
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
                symWidth=1.8
                symBorder=True
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
        fill=None;fillcolor=None
        if dataset['x4lbl'].find('/data')>=0:
            symBorder=False
            msize1=3
            iSymPlus=100  #-open
            fill='tozeroy'; fillcolor='rgba(0,0,255,0.1)'
            if dataset['x4lbl'].find('/data-max')>=0: fillcolor='rgba(255,0,0,0.1)'
        lbl=lblPrefix+str(ii+1)+') '+flagModif0+dataset['x4lbl']+' pt:'+str(len(dataset['x']))\
		+' x4:'+dataset['DatasetID']+flagModif1
#		+' #'+dataset['DatasetID']+flagModif1
        row0=dataset.get('row0')
        if row0 is not None:
            corr_author=row0.get('corr_author')
            if corr_author is not None: lbl='['+corr_author+']: '+lbl
        #tr=Scatter(x=dataset['x'],y=dataset['y'],error_y=error_y,error_x=error_x
        tr=Scatter(x=dataset['x'],y=dataset['y']
	,text=dataset['x4lbl']
	,name=lbl
	,marker_symbol=str((ii%25)+iSymPlus)
#	,marker_symbol=str((ii%33)+iSymPlus)
	,marker_size=msize1,mode="markers"
		,fill=fill,fillcolor=fillcolor
	)
        if dataset.get('dx') is not None: tr.error_x=dict(type='data',array=dataset['dx'],visible=True,thickness=0.9)
        if dataset.get('dy') is not None: tr.error_y=dict(type='data',array=dataset['dy'],visible=True,thickness=0.8)
        if dataset.get('DatasetSplit') is not None: tr.name+=' '+dataset['DatasetSplit']
        if (lines): tr.mode="markers+lines"
        if (lwidth>0): tr.line=dict(width=lwidth)
#        if (symBorder): tr.marker.line=dict(color='Black',width=0.8);tr['marker_symbol']='circle-open'
        if (symBorder): tr.marker.line=dict(color=symColor,width=symWidth)
        if (groupReac):
            if dataset['Reacode']!=lastReacode:
                iir+=1
                lastReacode=dataset['Reacode']
            tr.legendgroup='exGrp'+str(iir)
            tr.legendgrouptitle.text=""+dataset['Reacode']
        data1.append(tr)
        if hiden0: tr.visible='legendonly'
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

    #If you have problems with offline plot, try to uncomment next line:
    #how2plot=2

    if not filename.endswith('.html'): filename=filename+'.html'
    plot1={}
    plot1['data']=data1
    xaxis=dict(title=xtitle,showline=True,linecolor='black'
	,ticks='outside',showgrid=True,gridcolor='#aaaaaa',type=xtype)
    yaxis={'title':ytitle,'showline':True,'linecolor':'black'
	,'showgrid':True, 'gridcolor':'#aaaaaa','ticks':'outside','type':ytype
	,'zeroline':True, 'zerolinecolor':'#dddddd'#, 'zerolinewidth':0.1
	}

    xaxis['mirror']='ticks'
    yaxis['mirror']='ticks' 
    yaxis['zeroline']=True;    yaxis['zerolinecolor']="#AAAAAA";    yaxis['zerolinewidth']=1
    xaxis['zeroline']=True;    xaxis['zerolinecolor']="#AAAAAA";    xaxis['zerolinewidth']=1
    if xstep30: #display xticks with step 30
        xaxis['tick0']=0
        xaxis['dtick']=30

    if xrange is not None:
        if (xtype!='log'): xaxis['range']=xrange
        else: xaxis['range']=[math.log10(xrange[0]),math.log10(xrange[1])]
    if yrange is not None:
        if (ytype!='log'): yaxis['range']=yrange
        else: yaxis['range']=[math.log10(yrange[0]),math.log10(yrange[1])]

    annotations=None
    if (annot1 is not None):
        txt,x,y=annot1
        if (xtype=='log'): x=math.log10(x)
        if (ytype=='log'): y=math.log10(y)
        annotations=[dict(text=txt,x=x,y=y,font_size=32,showarrow=False,font_color='#0000FF')]
    plot1['layout']=Layout(title=ptitle
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
	,annotations=annotations
	)

    if how2plot==1:
        plotly.offline.plot(plot1,filename=filename)
    elif how2plot==2:
        fig=go.Figure(data=plot1['data'],layout=plot1['layout'])
        fig.write_html(filename)
        fig.show()

    #needs: $ pip3 install -U kaleido
    print("Will try---write_image: "+filename+".png")
    try:
        plotly.io.write_image(plot1,filename+'.png',width=1300,height=830)
    except Exception as ex:
        sys.stderr.write("---plotly.io.write_image---Exception-error: "+str(ex)+"\n")
        rows=[]
