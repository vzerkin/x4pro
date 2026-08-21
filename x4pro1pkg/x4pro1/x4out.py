"""
 *******************************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA)          *
 * Copyright: (C) 2023-2025 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2025) *
 *******************************************************************************
"""

import json
import datetime

#_________________Output EXFOR datasets ver.2025-01-23_________________
def outX4Datasets(datasets,filename='temp',frmArray=1):
    if frmArray==1:
        save1obj2file(datasets,filename)
        return
    if not filename.endswith('.json'): filename=filename+'.json'
    ts=str(datetime.datetime.now())[:19]
    ff=open(filename,'w')
    ff.write('{\n')
    ff.write('  "now":"'+ts.replace(' ','T')+'"'+'\n')
    ff.write(' ,"program":"X4Pro, by V.Zerkin, Vienna, ver.2025-01-23"\n')
    ii=0
    ff.write(' ,"datasets":[\n')
    for ds in datasets:
        #if ds['DatasetID']!='30114006': continue
        #print('outX4Datasets:'+filename+' ---DatasetID:'+ds['DatasetID'])
        #save1obj2file(ds,filename+'--obj')
        ss='  '
        if ii==0: ss+=' '
        else: ss+=','
#        ss+=json.dumps(ds,indent=2)
        ss+=ds2str(ds)
        ff.write(ss)
        ff.write('\n')
        ii+=1
    ff.write('  ]\n')
    ff.write('}\n')
    ff.close()
#    with open(filename,'w') as outfile:
#        json.dump(datasets,outfile,indent=2)
#    print(json.dumps(d4.allDicts,indent=2))

def ds2str(ds):
    x=[]; y=[]; dx=[]; dy=[]; fc=[]
    tab1='\t'
    i=0; sout='{\n'
    for ii,key in enumerate(ds):
        val=ds[key]
        if key=='x':         x=val;  continue
        if key=='y':         y=val;  continue
        if key=='dx':        dx=val; continue
        if key=='dy':        dy=val; continue
        if key=='FcApplied': fc=val; continue
        sout+='    '
        if i==0: sout+=' '
        else: sout+=','
        sout+='"'+key+'":'
        s1=json.dumps(val,indent=2)
        sout+=s1.replace('\n','\n    ')
        sout+='\n'
        i+=1
    ll=len(x)
    fstr='<12g'
    sout+='    ,"x_y_dy_dx_fc":[\n'
    i=0
#    print('ds2str---DatasetID:'+str(ds['DatasetID'])+' lx='+str(len(x))+' ly='+str(len(y))+' ldx='+str(len(dx))+' ldy='+str(len(dy)))
    for ii in range(ll):
#?        sout+='\t'
        sout+=tab1
        if i==0: sout+=' [ '
        else:    sout+=',[ '
        y1=0; dy1=0; dx1=0; fc1=1
        x1=x[i]
        if ii<len(y): y1=y[i]
        if ii<len(dy): dy1=dy[i]
        if ii<len(dx): dx1=dx[i]
        if ii<len(fc): fc1=fc[i]

        if dy1 is None: dy1=0
        if dx1 is None: dx1=0

        sout+=format(x1,fstr)
        sout+=' ,'+format(y1,fstr)

        if dy1!=0 or dx1!=0 or fc1!=1:
            sout+=' ,'+format(dy1,fstr)
            if dx1!=0 or fc1!=1:
                sout+=' ,'+format(dx1,fstr)
                if fc1!=1:
                    sout+=' ,'+format(fc1,fstr)

        sout+=']\n'
        i+=1
    sout+='    ]\n'
    sout+='  }'
    return sout


def save1obj2file(obj1,filename='temp'):
    if not filename.endswith('.json'): filename=filename+'.json'
    with open(filename,'w') as outfile:
        json.dump(obj1,outfile,indent=2)
