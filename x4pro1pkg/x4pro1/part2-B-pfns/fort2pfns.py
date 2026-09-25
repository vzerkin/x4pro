"""
 **************************************************************
 * Originally written on Fortran by Dr. Andrej Trkov (IAEA)   *
 *      as part of the projects: ENDVER and EMPIRE.           *
 * Adopted to Python by Dr. Viktor Zerkin for X4Pro examples. *
 * License:  MIT License (MIT)                                *
 **************************************************************
"""
import sys
import math
import json
sys.path.append('./')
sys.path.append('../')

def generateMxwCur(TMXW=1.32e6,E0=0.01,EL=1e-5,EH=30e6,verbose=False):
    #---adopted from MXWCUR.F (A.Trkov:EndVer/Empire-codes)
    PW=0.5
    MXNP=901
    obj={}
    obj['TMXW']=TMXW
    obj['E0']=E0
    obj['EL']=EL
    obj['EH']=EH
    obj['MXNP']=MXNP
    ENR=[]; XSP=[]
    obj['ENR']=ENR
    obj['XSP']=XSP
    ENR.append(0)
    XSP.append(0)
    EE=E0
    FE=math.exp(math.log(EH/E0)/(MXNP-2))
    def ThrMxw(E,T,PWR):
        P1=PWR+1
        THRMXW=(T**(-P1)/math.gamma(P1))*(E**PWR)*math.exp(-E/T)
#       print('---ThrMxw\t'+' E:'+format(E,"<11.5g")+' THRMXW:'+format(THRMXW,"<11.5g"))
        return THRMXW
    ii=1
    while ii<MXNP:
        FF=ThrMxw(EE,TMXW,PW)
        ENR.append(float(format(EE,".7e")))
        XSP.append(float(format(FF,".7e")))
        if verbose: print('---MxwCur:'+str(ii).ljust(4)+' EE='+format(EE,"<13.7e")+"  XSP="+format(FF,"<13.7e"))
        EE=EE*FE
        ii+=1
    return obj

def FITGRD(NEP1,EN1,XS1,NEP2,EN2,verbose=False):
    #---adopted from LSTTAB.F (A.Trkov:EndVer/Empire-codes)
    if verbose: print('---FITGRD---'+' NEP1='+str(NEP1)+"  NEP2="+str(NEP2))
    XS2=[0]*NEP2
    j1=0; j2=0
    while j2<NEP2:
        e2=EN2[j2]
        e1=EN1[j1]
        f1=XS1[j1]
        if e1==e2:
            XS2[j2]=f1
            if verbose: print('--fitgrd.copy',' j2:',j2,' j1:',j1,e1,' xs:',f1)
            if j1<NEP1-1: j1+=1
            j2+=1
        elif e1>e2: #interpolation
            jj=j1-1
            ff=0
            if jj>=0: ff=XS1[jj]+(f1-XS1[jj])*(e2-EN1[jj])/(e1-EN1[jj])
            ff=float(format(ff,".7e"))
            XS2[j2]=ff
            if verbose: print('--fitgrd.interpolation',' j2:',j2,' j1:',j1,' e2:',format(e2,"<13.7g"),' xs:',ff)
            j2+=1
        else:
            if j1<NEP1-1:
                if verbose: print('---fitgrd.skip---',' j2:',j2,' j1:',j1,' e1:',format(e1,"<13.7g"),' e2:',format(e2,"<13.7g"))
                j1+=1
            else:
                XS2[j2]=0
                if verbose: print('---fitgrd.zero---',' j2:',j2,' j1:',j1,' xs:',0)
                j2+=1
    return XS2

def YTGPNT(np,xx,yy,xa,xb,verbose=False):
    #---adopted from LSTTAB.F (A.Trkov:EndVer/Empire-codes)
    i=0; sum=0; x2=0; y2=0
    while i<np:
        x1=x2;    y1=y2
        x2=xx[i]; y2=yy[i]
        i+=1
        if i==1: x1=x2; y1=y2; continue
        if x2<xa: continue
        if x1<xa:
            if x2!=x1: y1=y1+(xa-x1)*(y2-y1)/(x2-x1)
            x1=xa
        if x2<=xb:
            sum+=(x2-x1)*(y2+y1)/2
            if verbose: print('-YTGPNT-'+str(i)+' sum:',format(sum,"<13.7g")+' plus:',format((x2-x1)*(y2+y1)/2,"<13.7g")+' x2-x1:',format(x2-x1,"<13.7g"))
        else:
            if x2!=x1: y2=y1+(xb-x1)*(y2-y1)/(x2-x1)
            x2=xb
            sum+=(x2-x1)*(y2+y1)/2
            if verbose: print('=YTGPNT='+str(i)+' sum:',format(sum,"<13.7g")+' plus:',format((x2-x1)*(y2+y1)/2,"<13.7g")+' x2-x1:',format(x2-x1,"<13.7g"))
            break
    return sum
