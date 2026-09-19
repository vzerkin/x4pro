import os
import sys
import json
import math

def readFileZvdat(fileName,verbose=False):

    def str2float(str1):
        if str1 is None: return None
        try: rr=float(str1)
        except ValueError: rr=None
#       print("   ---str2float:["+str1+"] --> "+str(rr))
        return rr

    def str2floats(str1):
        if str1 is None: return []
        arr=[]
        ii=str1.find('#')
        if ii>=0: str1=str1[:ii]
        words=str1.strip().split()
#       print("   ---str2floats:["+str1+"] --> "+str(words))
        for word in words:
            try:
                rr=float(word)
                arr.append(rr)
            except ValueError: pass
#       print("   ---str2floats:["+str1+"] --> "+str(arr))
        return arr

    date=''; time=''
    Ei=-1; Target=''; fx=1; fy=1; idy=0; x=[]; y=[]; dy=[]; dx=[]
    datasets=[]
    dataset=None
    try: ff=open(fileName,"r")
    except Exception as e:
        sys.stderr.write("===ERROR===Exception: "+str(e)+"\n")
        return None
    obj0={}
    obj0['fmt']='ZVView-data-copy'
    obj0['ts']=''
    obj0['datasets']=datasets
    iline=0
    while True:
        line=ff.readline()
        if not line: break
        iline+=1
        line=line.rstrip('\n')
        words=line.strip().split()
        if line.startswith('#ZVView-data-copy'):
            date=''; time='';
            if len(words)>1: date=words[1]
            if len(words)>2: time=words[2]
            obj0['ts']=date+' '+time
            continue
        if line.startswith('#name:'): #name: ENDF/B-VIII.1: U-235(N,F) E_in=1.e-11 MeV
            lib=''; Target=''; Ei=0
            fx=1; fy=1; idy=0; x=[]; y=[]; dy=[]; dx=[]
            if len(words)>1:
                lib=words[1]
                if lib.endswith(':'): lib=lib[:-1]
            if len(words)>2:
                txt=words[2]
                Target=txt
                iii=txt.find('(')
                if iii>0: Target=txt[:iii]
            if len(words)>3:
                txt=words[3].replace('E_in=','')
                Ei=str2float(txt)
            if verbose: print(iline,'#name:',lib,Target,Ei)
            continue
        if line.startswith('#data...'):
#           print(iline,'#data...',line)
            line=ff.readline() # X Y dY
            line=ff.readline() # eV 1/eV 1/eV
            if not line: break
            words=line.upper().strip().split()
#           print(iline,'---UNITS---',line,len(words),words)
            if len(words)>2:
                if words[1]=='MEV':   fx=1e6
                if words[1]=='KEV':   fx=1e3
                if words[2]=='1/MEV': fy=1e-6
            dataset={}
            dataset['DatasetID']='1111111'
            dataset['lib']=lib
            dataset['DATE']=""
            dataset['AUTH']=""
            dataset['myColor']="255,0,0|solid"
            dataset['TARGET']=Target
            dataset['x4lbl']=lib+" Ei:"+format(Ei*1e6,"<.4g").strip()
            dataset['Ei']=float(format(Ei*1e6,"<.6e"))
            dataset['fx']=fx
            dataset['fy']=fy
            dataset['idy']=idy
            dataset['x']=x
            dataset['y']=y
            dataset['dy']=dy
            continue
        if line.startswith('//'):
            if dataset is not None:
                dataset['idy']=idy
                print("---read-zvd.dat:dataset-"+str(len(datasets)).ljust(3)+" --> Lib:"+lib+" Target:"+Target+" Ei:"+str(Ei)+" x:"+str(len(x))+" fx:"+str(fx)+" idy:"+str(idy))
                datasets.append(dataset)
            continue
        arr=str2floats(line)
        if len(arr)>=2:
            if arr[0]==0: continue
            x.append(arr[0])
            y.append(arr[1])
            if len(arr)>=3: dy.append(arr[2]); idy+=1;
            else: dy.append(None)
    ff.close()
    return obj0

def cmpGrid(x1,x2):
    if len(x1)!=len(x2): return False
    for ii,e1 in enumerate(x1):
        if e1!=x2[ii]: return false
    return True

def interploateZvdat(xObj,Ei,verbose=False):
    print("===interploateZvdat===Ei:"+str(Ei))
    datasets=xObj['datasets']
    if len(datasets)<1: return None
    if len(datasets)==1: return datasets[0]
    str0Ei=format(Ei,"<.6g").strip()
    w1=None
    for ii,dataset in enumerate(datasets): #find equal
        EE=dataset['Ei']
        str1Ei=format(EE,"<.6g").strip()
#       print("??Ei:["+str0Ei+"]cmp:["+str1Ei+"]")
        if EE==Ei: return dataset
    for ii,dataset in enumerate(datasets): #interpolate
        if ii==0:
            E1=dataset['Ei']
            ds1=dataset
            if Ei<E1: return None
            continue
        E2=dataset['Ei']; ds2=dataset
        if Ei>=E1 and Ei<=E2:
            w1=(Ei-E1)/(E2-E1); w2=1-w1
            print("---interploateZvdat---Ei:"+str(Ei)+" E1:"+str(E1)+" E2:"+str(E2)+" w1:"+str(w1))
            if cmpGrid(ds1['x'],ds2['x']):
                ds=ds1.copy()
                for iii,y1 in enumerate(ds1['y']):
                    y2=ds2['y'][iii]
                    y=y1+w1*(y2-y1)
                    y=float(format(y,"<.6e"))
                    ds['y'][iii]=y
                    print("///interploateZvdat---E:"+str(ds1['x'][iii])+" y1:"+str(y1)+" y2:"+str(y2)+" w1:"+str(w1)+" y="+str(y))
                    dy1=ds1['dy'][iii]
                    dy2=ds2['dy'][iii]
                    if dy1 is None: continue
                    if dy2 is None: continue
                    dy=dy1+w1*(dy2-dy1)
                    ds['dy'][iii]=float(format(dy,"<.6e"))
                ds['x4lbl']=dataset['lib']+" Ei:"+format(Ei,"<.4g").strip()
                ds['Ei']=float(format(Ei,"<.6e"))
                return ds
            if w1<0.5: return ds1
            else: return ds2
        E1=E2; ds1=ds2
    return None


def readZvdatSp1(zvdatCurFile,iCurve,Ei,T=1.32e6):
    xObj=readFileZvdat(zvdatCurFile)
    if xObj is None: return None
    print('---readZvdatSp1---',zvdatCurFile,' #Datasets:',len(xObj['datasets']))
    sys.stderr.write('---readZvdatSp1---'+str(zvdatCurFile)+' #Datasets:'+str(len(xObj['datasets']))
	+' iCurve:'+str(iCurve)+' Ei:'+str(Ei)+' T:'+str(T)+'\n')
    dataset=interploateZvdat(xObj,Ei)
#   with open(fname+".ds-"+Ei,"w") as FF: json.dump(dataset,FF,indent=1)
    if dataset is None: return None
    ds=dataset
#    if iCurve==0: ds['myColor']="255,0,0|solid"
    if iCurve==0: ds['myColor']="0,0,0|solid"
    if iCurve==0: ds['myColor']="255,0,0|solid|5"
    if iCurve==1: ds['myColor']="0,255,255|longdashdot"
    if iCurve==2: ds['myColor']="0,160,0|dot"
    if iCurve==3: ds['myColor']="0,0,160|dot"
    col=getCurveColor(ds,iCurve)
    if col is not None: ds['myColor']=col
    if T<=0: return dataset
    x=dataset['x']
    y=dataset['y']
    dy=dataset['dy']
    fx=dataset['fx']
    for ii,xx in enumerate(x):
        yy=y[ii]
        dyy=dy[ii]
        E=xx*fx
        FC=(2/T)*math.sqrt(E/(math.pi*T))*math.exp(-E/T)
        if dyy is not None:
            print('$$T:'+str(T)+' ##E:'+format(E,"<.5e")+' ##Y:'+format(yy,"<.4g").strip()+' ##dY:'+format(dyy,"<.4g").strip()+' ##FC:'+format(FC,"<.4g").strip())
        else:
            print('$$T:'+str(T)+' ##E:'+format(E,"<.5e")+' ##Y:'+format(yy,"<.4g").strip()+' ##FC:'+format(FC,"<.4g").strip())
        yy=yy/FC # *1e6
        yy=float(format(yy,".5e"))
        if dyy is not None:
            dyy=dyy/FC # *1e6
            dyy=float(format(dyy,".5e"))
        y[ii]=yy
        dy[ii]=dyy
        x[ii]=E/1e6
    ds=dataset
    ds["Tmxw"]=T
    ds["fx"]=1e6
    ds["fy"]=1
    if T<=0:
        ds['x4lbl']+=" /spectrum/"
    else:
        ds['x4lbl']+=" (T="+format(T/1e6,"<.5g").strip()+"MeV)"
    return dataset

def getCurveColor(ds,iCurve):
    color=None
    libColors={
	'ENDF/B-VIII.0':"0,0,255|solid|2",	#dash | dot | dashdot
 	'ENDF/B-VIII.1':"0,0,255",
	'ENDF/B-VII.1':"200,0,255|dashdot|2",
	'INDEN-Aug2023':"0,80,255",
	'JENDL-5':"0,200,0",
	'JENDL-4.0':"0,200,127|dashdot",
	'JEFF-4.0':"255,0,0",
	'JEFF-3.3':"0,255,255",
	'JEFF-3.1':"0,255,255",
	'JEF-2.2':"0,255,255",
	'CENDL-3.2':"255,0,0",
	'CENDL-2':"255,0,0",
	'BROND-3.1':"255,0,255",
	'ENDF/B-V':"127,127,127",
	'MINKS-ACT':"255,80,80|dashdot",
	'Minsk-Actinides':"255,40,127|solid|6"
	}
    lib=ds['lib']
    color=libColors[lib]
    return color

def main():
    print("Program: readZvdat.main #self-test")

    fname="u235nf-ENDF_B-VIII.1.zvd.dat"
    if (len(sys.argv)>1) and (sys.argv[1]!=''): fname=str(sys.argv[1])
    print("Reading: "+fname)
    print("Wait...")

    xObj=readFileZvdat(fname)
    print('---#Datasets:',len(xObj['datasets']))
    with open(fname+".json","w") as FF: json.dump(xObj,FF,indent=1)
    dataset=interploateZvdat(xObj,0.0253)
    with open(fname+".ds-therm","w") as FF: json.dump(dataset,FF,indent=1)
    dataset=interploateZvdat(xObj,7e6)
    with open(fname+".ds7","w") as FF: json.dump(dataset,FF,indent=1)
    dataset=interploateZvdat(xObj,7.4e6)
    with open(fname+".ds74","w") as FF: json.dump(dataset,FF,indent=1)
    dataset=interploateZvdat(xObj,50e6)
    with open(fname+".ds50","w") as FF: json.dump(dataset,FF,indent=1)
    print('\nProgram completed.')

if __name__ == '__main__':
    main()
