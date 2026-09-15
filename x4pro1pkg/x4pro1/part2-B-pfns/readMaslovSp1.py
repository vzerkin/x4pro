import os
import sys
import math

def readMaslovSp1(fileName):
    T=1.32e6
    Einc=-1
    x=[]; y=[]; dy=[]; dx=[]
    ff=open(fileName,"r")
    ii=0
    for line in ff:
        line=line.rstrip('\n')
        line=line.strip()
        if line=='': continue
        ii+=1
        if line.startswith('#'): continue
        arr=[]; words=[]
        for t in line.split():
            words.append(t)
            try: arr.append(float(t))
            except ValueError: pass
        if line.startswith('EN='):
            Einc=arr[0] #MeV
            continue
        if ii<5: continue
        if len(arr)<2: continue
        xx=arr[0]
        yy=arr[1]
        if xx==0: continue
        if xx==20 and yy==0: continue
        E=xx*1e6
        FC=(2/T)*math.sqrt(E/(math.pi*T))*math.exp(-E/T)
        print('##T'+str(T)+' ##E:'+str(E)+' ##FC:'+str(FC))
        yy=yy/FC*1e-6
        yy=float(format(yy,".5e"))
        dyy=0
        x.append(xx)
        y.append(yy)
        dy.append(dyy)
    ff.close()
    ds={
	  "DatasetID": 999924020202,
	  "myColor": "255,0,0|longdashdot",
	  "TARGET": "U-235",
	  "MF": 5,
	  "MT": 18,
	  "fx": 1000000.0,
	  "fy": 1.0,
	  "x4lbl": "Minsk-Actinides Ei:"+str(Einc)+"MeV (T=1.32MeV)",
	  "DATE": "2026",
	  "AUTH": "2026 V.Maslov"
    }
    ds['idy']=0
    ds['x']=x
    ds['y']=y
    ds['dy']=dy
    return ds
