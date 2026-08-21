"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2024 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2024) *
 *******************************************************************************
"""

import matplotlib.pyplot as plt

def prepareEndfDataForPlot(datasets,legendgroup,dy_showlegend,autocolor=False,lwidth=4,showAuth=False):
    ldata=len(datasets)
    ii=0; data1=[]
    for dataset in datasets:
        #if (len(dataset['x'])<=1): continue
        #plt.scatter(dataset['x'],dataset['y'], s=60, c='red', marker='^')
        mrk='.'
        mrk=' '
        lbl=str(ii+1)+') '+dataset['x4lbl']
        if showAuth: lbl+=' '+dataset['AUTH']
        lbl+=' pt:'+str(len(dataset['x']))
        if dataset.get('DatasetSplit') is not None: lbl+=' '+dataset['DatasetSplit']

        if autocolor: mycolor=None
        else:
            i3=[int(ii3) for ii3 in dataset['myColor'].split(',')]
            mycolor='#'+str("%02X"%i3[0])+str("%02X"%i3[1])+str("%02X"%i3[2])
        #print('myColor:'+dataset['myColor']+' mycolor:',mycolor)
        if (dataset['idy']>0):
            x=dataset['x'];
            y=dataset['y'];
            dy=dataset['dy'];
            lx=len(x)
            y_upper=[];y_lower=[]
            for i2 in range(lx): y_upper.append(y[i2]+dy[i2])
            for i2 in range(lx): y_lower.append(y[i2]-dy[i2])
            plt.fill_between(x,y_lower,y_upper,color=mycolor,alpha=0.2)
        plt.plot(dataset['x'],dataset['y']
		,markersize=1, marker=mrk
		,linestyle='-',linewidth=lwidth/2
		,label=lbl
		,color=mycolor,alpha=0.8
	)
        ii+=1
    return data1
