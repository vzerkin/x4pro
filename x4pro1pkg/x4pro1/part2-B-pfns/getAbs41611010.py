def getAbs41611010():
    txt0='''
#92-U-233(N,F),PR,NU/DE,,MXD 41611010 En=3.63e-8MeV T=1.34MeV 2016 Vorobyev
#Total PFNS of 233U(n, f)
#En       <FF>*10^4  D<FF>
#MeV      Neutr/MeV  %
16.650    0.25833    36.6 
13.290    3.0781     23.0 
10.860    14.846     16.3 
9.043     54.140     12.8 
7.647     155.58     9.9  
6.552     339.32     8.1  
5.677     638.37     6.9  
4.967     1014.9     5.6  
4.383     1547.5     4.8  
3.896     2099.4     4.1  
3.486     2666.2     3.5  
3.137     3277.0     3.3  
2.839     3871.4     2.9  
2.581     4525.8     2.7  
2.357     5174.1     2.5  
2.161     5537.1     2.2  
1.988     6167.8     2.2  
1.835     6529.2     2.1  
1.699     6987.9     2.0  
1.578     7203.9     2.2  
1.469     7233.0     2.1  
1.372     7801.3     2.3  
1.283     7930.2     1.8  
1.203     8009.8     2.1  
1.130     8349.3     1.9  
1.064     8346.4     2.3  
1.003     8365.0     2.6  
0.948     8523.4     2.4  
0.896     8470.3     3.0  
0.849     8659.7     2.7  
0.806     8700.3     3.0  
0.766     8522.9     3.0  
0.728     8868.0     2.8  
0.694     8772.8     3.1  
0.661     8725.0     3.1  
0.631     8455.9     2.9  

0.603     8683.1     3.2
0.577     8659.9     3.4
0.553     8660.3     3.5
0.530     8686.6     3.7
0.488     8573.7     2.8
0.434     8269.2     3.2
0.388     7720.0     3.9
0.349     7983.4     4.7
0.316     7882.1     5.0
0.287     7322.5     6.0
0.263     7290.6     6.9
0.241     6594.0     7.8
0.221     7118.3     9.6
'''
    x=[]; y=[]; dy=[]; dx=[]
    for line in txt0.split('\n'):
        line=line.strip()
        if line=='': continue
        if line.startswith('#'): continue
        arr=[]
        for t in line.split():
            try: arr.append(float(t))
            except ValueError: pass
        if len(arr)<3: continue
        xx=arr[0]
        yy=arr[1]*1e-4*1e-6
        yy=float(format(yy,".5e"))
        dyy=yy*arr[2]/100
        dyy=float(format(dyy,".5e"))
#        yy=arr[1]
#        dyy=arr[2]
        x.append(xx)
        y.append(yy)
        dy.append(dyy)
        dx.append(None)
    ds={
    "DatasetID": "41611010z",
    "Reacode": "92-U-233(N,F),PR,NU/DE",
    "Target": "U-233",
    "Reaction": "N,F",
    "Quantity": "Energy spectrum of prompt fission neutrons",
    "xBasicUnits": "EV",
    "yBasicUnits": "PC/FIS/MEV",
    "xexpansion": "Secondary energy: particle energy",
    "yexpansion": "Data: data",
    "Quant": "MFQ",
    "SF8": "",
    "MF": 5,
    "MT": 18,
    "yformula": "y=DATA(EN,E2)",
    "DatasetSplit": "",
    "g0": 0.0363,
    "g1": 0,
    "En": 0.0363,
    "YearRef1": 2016,
    "Author1Ini": "A.S.",
    "Author1": "Vorobyev",
    "x4lbl": "2016, A.S.Vorobyev Einc:0.0363eV T=1.34MeV",
    "fx": 1000000.0,
    "fy": 1.0,
    }
    x.reverse()
    y.reverse()
    dy.reverse()
    ds['x']=x
    ds['y']=y
    ds['dy']=dy
    ds['dx']=dx
    if False:
        print('---reprint data---')
        for ii,xx in enumerate(x):
            yy=y[ii]; dyy=dy[ii]
            print(format(xx,"6.3f")+'     '+format(yy,"<11.5g")+'     '+format(dyy,"3.1f"))
    return ds
