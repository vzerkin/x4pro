import os
import sys
import json
import math

def readFileExpData(fileName,fx0=1e6,fy0=1,verbose=False):
    #reading JSON file with external experimental data (may have sevaral datasets)
    print("---readFileExpData/json: "+fileName)

    obj0=None
    try:
        with open(fileName, encoding='utf-8') as F:
            obj0=json.loads(F.read())
    except Exception as e:
        print("===Exception==="+str(e))
        return []

    if obj0 is None: return []
    datasets=obj0.get('datasets')
    print("---readFileExpData: ",len(datasets))
    if datasets is None: return []
    dss=[]
    for ids,ds in enumerate(datasets):
        arr=ds.get('x_y_dy_dx_fc')
        if arr is None: continue
        x=[]; y=[]; dy=[]; dx=[]
        fx=ds['fx']
        if fx is None: fx=1
        fy=ds['fy']
        if fy is None: fy=1
        sys.stderr.write("---readFileExpData---fx="+str(fx)+" fy:"+str(fy)+"\n")
        for ii,arr1 in enumerate(arr):
            if len(arr1)<2: continue
            xx=arr1[0]*fx/fx0
            yy=arr1[1]*fy/fy0
            yy=float(format(yy,".7e"))
            if len(arr1)>2: dyy=arr1[2]*fy; dyy=float(format(dyy,".7e"))
            else: dyy=None
            if len(arr1)>3: dxx=arr1[3]*fx; dxx=float(format(dxx,".7e"))
            else: dxx=None
            x.append(xx)
            y.append(yy)
            dx.append(dxx)
            dy.append(dyy)
#       del ds('x_y_dy_dx_fc')
        ds.pop('x_y_dy_dx_fc')
        ds.pop('initialData')
        DatasetID=ds.get('DatasetID')
        if DatasetID is None: ds['DatasetID']='77777.'+str(ids+1)
        ds['x']=x
        ds['y']=y
        ds['dy']=dy
        ds['dx']=dx
        ds['fx']=fx
        ds['fy']=1
        dss.append(ds)
    return dss

def main():
    print("Program: readExpData.main #self-test")

    fname="exp41171004.txt"
    if (len(sys.argv)>1) and (sys.argv[1]!=''): fname=str(sys.argv[1])
    print("Reading: "+fname)
    print("Wait...")

    dss=readFileExpData(fname)
    print('---#Datasets:',len(dss))
    with open(fname+".json","w") as FF: json.dump(dss,FF,indent=1)
    print('\nProgram completed.')

if __name__ == '__main__':
    main()
