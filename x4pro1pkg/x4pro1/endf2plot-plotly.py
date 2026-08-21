"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2024 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2024) *
 *******************************************************************************
"""

import plotly 
from plotly.graph_objs import Scatter, Layout 

def prepareEndfDataForPlot(datasets,legendgroup,dy_showlegend,autocolor=False,lwidth=4,showAuth=False):
    ldata=len(datasets)
    ii=0; data1=[]
    for dataset in datasets:
        #if (len(dataset['x'])<=1): continue
        trErr=None
        if (dataset['idy']>0):
            x=dataset['x'];
            y=dataset['y'];
            dy=dataset['dy'];
            lx=len(x)
            x_rev=x[::-1]
            y_upper=[];y_lower=[]
            for i2 in range(lx): y_upper.append(y[i2]+dy[i2])
            for i2 in range(lx): y_lower.append(y[lx-i2-1]-dy[lx-i2-1])
            trErr=Scatter(x=x+x_rev,y=y_upper+y_lower
		,text=dataset['x4lbl']
		,name='err-'+str(ii+1)+') '+dataset['x4lbl']+' pt:'+str(len(dataset['x']))
		,mode="lines"
		,fill='toself'
		,fillcolor='rgba('+dataset['myColor']+',0.2)'
		,line=dict(width=0)
#		,showlegend=False
		)

        #myline=dict(color='rgba('+dataset['myColor']+',0.7)', width=4)
        if autocolor: myline=dict(width=lwidth)
        else: myline=dict(color='rgb('+dataset['myColor']+')', width=lwidth)
        name=str(ii+1)+') '+dataset['x4lbl']
        if showAuth: name+=' '+dataset['AUTH']
        name+=' pt:'+str(len(dataset['x']))
        tr=Scatter(x=dataset['x'],y=dataset['y']
		,text=dataset['x4lbl']
#2024		,name=str(ii+1)+') '+dataset['x4lbl']+' pt:'+str(len(dataset['x']))
		,name=name
#		,line=dict(color='rgb('+dataset['myColor']+')', width=3)
#		,line=dict(color='rgba('+dataset['myColor']+',0.7)', width=4, dash='dot')
#		,line=dict(color='rgba('+dataset['myColor']+',0.7)', width=4, dash='longdashdot')
#		,line=dict(color='rgba('+dataset['myColor']+',0.7)', width=4, dash='dashdot')
#		,line=dict(color='rgba('+dataset['myColor']+',0.7)', width=3, dash='dashdot')
	#	,line=dict(color='rgba('+dataset['myColor']+',0.7)', width=4)
		,line=myline
		,opacity=0.8
		,mode="lines"
#,legendgroup="group1"
#,legendgrouptitle_text="Evaluated data"
#,legendrank=ii
		)
        try: tr['legendrank']=ii
        except Exception as ex: print('Plotly version: '+plotly.__version__)
        if (legendgroup!=''):
            tr.legendgroup=legendgroup
            tr.legendgrouptitle.text="EVALUATED DATA"
            if (trErr is not None):
                trErr.legendgroup=legendgroup
                trErr.legendgrouptitle.text="EVALUATED DATA"
        if (trErr is None):
            data1.append(tr)
        else:
            if (not dy_showlegend):
                trErr.showlegend=False
                data1.append(trErr)
                data1.append(tr)
            else:
                trErr.showlegend=True
                data1.append(tr)
                #trErr.legendrank=ii
                try: trErr['legendrank']=ii
                except Exception as ex: print('Plotly version: '+plotly.__version__)
                #print('Plotly version: '+plotly.__version__)
                data1.append(trErr)
        ii+=1
        print('Plot:'+str(ii)+'/'+str(ldata)+') '+str(dataset['DatasetID'])+'\t'+str(dataset['x4lbl'])+'\tpt:'+str(len(dataset['x']))+'\tcolor:'+dataset['myColor'])

    return data1
