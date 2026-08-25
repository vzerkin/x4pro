
def fcorr_142710031(row):	#2010,F.Tovesson
    #Reaction: (94-PU-239(N,F),,SIG)/(92-U-235(N,F),,SIG)
    ene=row['En']
    if ene>13e6: 
        print("___________fcorr_142710031:"+' En='+str(row['En']/1e6)+'MeV'+' -REJECTED-')
        return -1		#data above 13 MeV rejected in Neutron Standard evaluation (2017)
    row['En']=row['En']*1.2	#just as example
    row['y']=row['y']*1.1	#just as example
#    print("___________fcorr_142710031:"+' En='+str(row['En']/1e6)+'MeV'+' -ACCEPTED-')
    return 1			#updated == accepted

def fcorr_41455005(row):	#x4u:20170724 #2002,O.Shcherbakov
    # REACTION   ((94-PU-239(N,F),,SIG)/(92-U-235(N,F),,SIG))
    # MONITOR    ((94-PU-239(N,F),,SIG)/(92-U-235(N,F),,SIG))
    # MONIT-REF  (,,3,JENDL-3.2,,1994)
    # COMMENT    Of Authors.
    #            The fission cross-section ratio normalization
    #            has been done in the 1.75-4.0 MeV energy interval
    #            using data of JENDL-3.2.
    y=row['y']
    dy=row['dy']
    dy=dy/y;		#convert abs. uncertainty in cs-ratio to rel. uncertainty
    a0=1.535;		#used ratio normalization factor (using data of JENDL-3.2), E:1.75-4.0 MeV
    c0=1.668/100;	#1.535 +-1.668% (this uncertainty is not included to error analys)
    a1=1.5393;		#ratio normalization factor (using data of ENDF/B-VIII.0), E:1.75-4.0 MeV
    c1=2.82/100;	#1.5393 +-2.82% (uncertainty should be added)
    fc=a0/a1; 		#total correction factor
    y=y*fc;		#correction exp. cs
    dy=dy**2+c1**2;	#calc. new quadrature of total uncertainty
    dy=dy**0.5*y;	#back to absolute uncertainty
    print("___________fcorr_41455005:"+' En='+str(row['En'])
	+'	y0='+str(row['y'])+'	y1='+str(round(y,5))+'	Fc='+str(round(fc,5))
	+'	dy0='+str(row['dy'])+'	dy1='+str(round(dy,5)))
    row['y']=y		#save y
    row['dy']=dy	#save dy
    return 1		#updated
