#Dataset:10224002

def corr_point(row):
    y  =row["y"]
    dy =row["dy"]
    if dy is None: dy=0
                #[K.Zolotarev 2011]
    #10224002   #1972 D.C.Santry+ 
                #measurements with T(p,n)He3 neutron source
                #monitor BF3 long counter
    a0=0.91582; #experimental data were renormalized to the integral of
                #cross-section calculated from experimental data of Mannhart
                #and Schmidt 2007 in the overlapping energy
                #range 1.500 - 3.958 MeV, a0=0.91582
    a1=0.0115;  #error in b+ mode in Cu64 decay - 1.15%
    a2=0.03;    #error in normalization value       - 3%
    a3=0.03;    #error in angular neutron intensity - 3%
                #error in the cs data due to the error in En center pozition
                #of 0.17 - 20.09% are not taken into accout 
    dy=dy/y;    #relative uncertainty in original cs for Zn64(n,p)Cu64 reaction 
    fc=a0;      #total correction factor                      
    y=y*fc;     #correction exp. cs
    dy=dy**2+a1**2+a2**2+a3**2; #determination the quadrature of new total error
    dy=dy**0.5*y; #determination the absolute error in new Zn64(n,p) cs
    row["y"]=y
    row["dy"]=dy
    return 1

