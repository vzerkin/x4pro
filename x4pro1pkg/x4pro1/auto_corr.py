"""
 **********************************************************************
 * Copyright: (C) 2021-2022 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""

def auto_corr_dataset(rows):
    newrows=[]
    if len(rows)<=0: return newrows
    row=rows[0]
    DatasetID=row['DatasetID']
    icmp=auto_corr_dataset_chkm0err(rows)
    print("___________auto_corr_dataset:::"+DatasetID+" len="+str(len(rows))+" icmp="+str(icmp))
    for row in rows:
#        print("___________auto_corr_data:::y="+str(row['y']))
        iupd=auto_corr_point(row,icmp)
        if iupd>0:
            newrows.append(row);
            row['corrected']=1
    return newrows

def auto_corr_dataset_chkm0err(rows):
    if len(rows)<=0: return 0
    for row in rows:
        icmp=auto_corr_point_chkm0err(row)
        if icmp!=0: return icmp
    return 0

def auto_corr_point_chkm0err(row):
    y0=row['y']
    dy=row.get('dy')
    if (dy is not None) and (y0>0):
        dm0=row.get('dm0')
        m0=row.get('m0')
        dm1=row.get('dm1')
        if (dm0 is not None) and (m0 is not None) and (dm1 is not None):
            if (dm0>0) and (m0>0):
                dyrel=dy/y0
                if (dm0/m0>=dyrel):
#                    print("\n__0_____dycorr:"+row['DatasetID']+' En='+str(row['En']/1e6)+'\tdm0/m0:'+str(dm0/m0)+'\t>=dyrel:'+str(dyrel))
                    return 1 #monerr>=dyrel (probably, monerr is included to dyrel)
    return 0 #ok for update

def auto_corr_point(row,icmp):
    y=row['y']
    y0=y
    fc=row.get('FcNew')
    print("\n__0________fcorr:"+row['DatasetID']+' En='+str(row['En']/1e6)+'\ty0='+str(y0)\
	+'\tfc='+str(fc)+'\tdy0='+str(row.get('dy','none'))+' icmp='+str(icmp))
    if fc is None: return 0 #unchanged
    y=y*fc;		#correction exp. cs
    row['y']=y
    dy=row.get('dy')
    if (dy is None): return 1
    if (icmp!=0):
        dy=dy*fc;	#correction dCS: rel=the same, absDY*=Fc
        print("__Fin:__1__fcorr:"+row['DatasetID']+' En='+str(row['En']/1e6)
	+'	y0='+str(y0)
	+'	y1='+str(round(y,7))
	+'	Fc='+str(round(fc,7))
	+'	dy0='+str(row['dy'])
	+'	dy1='+str(round(dy,7)))
        row['dy']=dy
        return 1 #updated
    if (y0!=0):
        m0=row.get('m0')
        dm0=row.get('dm0')
        m1=row.get('m1')
        dm1=row.get('dm1')
        if (m0 is not None) and (dm0 is not None) and (m1 is not None) and (dm1 is not None):
            dy=dy/y0
            dm0=dm0/m0
            dm1=dm1/m1
            print("__1________fcorr-err:"+row['DatasetID']+' dy='+str(round(dy*100,3))+' dm0='+str(round(dm0*100,3))+' dm1='+str(round(dm1*100,3)))
            if (dy>dm0):
                dy=dy**2-dm0**2+dm1**2; #determination the quadrature of new total error
            else:
                dy=dy**2+dm1**2; #determination the quadrature of new total error
            print("__2________fcorr-err:"+row['DatasetID']+' dy='+str(round((dy**0.5)*100,3)))
            dy=dy**0.5*y;	#determination the absolute value of new total error
    print("__Fin:__2__fcorr:"+row['DatasetID']+' En='+str(row['En']/1e6)
	+'	y0='+str(y0)
	+'	y1='+str(round(y,7))
	+'	Fc='+str(round(fc,7))
	+'	dy0='+str(row['dy'])
	+'	dy1='+str(round(dy,7)))
    row['dy']=dy
    return 1 #updated



def ratio2cs_dataset(rows):
    newrows=[]
    if len(rows)<=0: return newrows
    row=rows[0]
    DatasetID=row['DatasetID']
    print("___________ratio2cs_dataset:::"+DatasetID+" len="+str(len(rows)))
    for row in rows:
#        print("___________ratio2cs_datapoint:::y="+str(row['y']))
        iupd=ratio2cs_datapoint(row)
        if iupd>0:
            newrows.append(row);
            row['corrected']=1
    return newrows

def ratio2cs_datapoint(row):
    y=row['y']          #ratio
    m1=row.get('m1')
    dm1=row.get('dm1')
    if m1 is None: return -1 #remove
    if m1<=0:      return -1 #remove
    y1=y*m1;		#ratio * m1
    row['y']=y1         #save as 'y'
    dy=row.get('dy')
    if dy is None: return 1 #updated
    if dm1 is None: dm1=0
    dy2=(y*dm1)**2+(m1*dy)**2	#determination the quadrature of new total error
    dy1=dy2**0.5
    print("___________ratio2cs:"+' En='+str(row['En']/1e6)
	+'	y0='+str(round(y*1e3,5))
	+'	dy0='+str(round(dy/y*100,5))+'%'
	+'	m1='+str(round(m1*1e3,5))
	+'	dm1='+str(round(dm1/m1*100,5))+'%'
	+'	y1='+str(round(y1*1e3,7))
	+'	dy1='+str(round(dy1/y1*100,5))+'%'
	)
    row['dy']=dy
    return 1 #updated
