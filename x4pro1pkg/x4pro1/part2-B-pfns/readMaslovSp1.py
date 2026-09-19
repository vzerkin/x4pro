import os
import sys
import math

def readMaslovSp1(fileName,iCurve,T=1.32e6):
    Einc=-1
    x=[]; y=[]; dy=[]; dx=[]
    try: ff=open(fileName,"r")
    except Exception as e:
        sys.stderr.write("===ERROR===Exception: "+str(e)+"\n")
        return None
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
        if T>0:
            FC=(2/T)*math.sqrt(E/(math.pi*T))*math.exp(-E/T)
            print('##T:'+str(T)+' ##E:'+format(E,"<.5e")+' ##Y:'+format(yy,"<.4g").strip()+' ##FC:'+format(FC,"<.4g").strip())
            yy=yy/FC*1e-6
            yy=float(format(yy,".5e"))
        else: yy=yy*1e-6
#?      else: yy=yy*5e-6
        dyy=0
        x.append(xx)
        y.append(yy)
        dy.append(dyy)
    ff.close()
    ds={
	  "DatasetID": 999924020202,
#	  "myColor": "255,80,0|longdashdot",
#	  "myColor": "255,80,0|solid",
	  "myColor": "255,0,0|solid",
	  "lib": "Minsk-Actinides",
	  "TARGET": "U-235",
	  "MF": 5,
	  "MT": 18,
	  "Tmxw": T,
	  "fx": 1000000.0,
	  "fy": 1.0,
	  "x4lbl": "Minsk-Actinides Ei:"+str(Einc)+"MeV (T="+format(T/1e6,"<.5g").strip()+"MeV)",
	  "DATE": "2026",
	  "AUTH": "2026 V.Maslov"
    }
    if T<=0:
        ds['x4lbl']="Minsk-Actinides Ei:"+str(Einc)+"MeV /spectrum/"
#   if iCurve==1: ds['myColor']="255,100,100|longdashdot"
#    if iCurve==1: ds['myColor']="255,63,63|dot|5"
    if iCurve==1: ds['myColor']="255,0,0|solid|7"
    if iCurve==2: ds['myColor']="255,63,63|dash|4"
    ds['idy']=0
    ds['x']=x
    ds['y']=y
    ds['dy']=dy
    return ds
