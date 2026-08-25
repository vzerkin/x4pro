"""
 *******************************************************************************
 * Copyright: (C) 2025-2026 Viktor Zerkin, Vienna, Austria                     *
 * Author: Viktor Zerkin, v.zerkin@gmail.com, IAEA(1999-2023), NRDC(1996-2026) *
 * License:  MIT License (MIT)                                                 *
 *******************************************************************************
"""

#EXFOR precision: 11 columns = 6 digits: 1.23456e-02
#multiply C5 data with C5 precision
def c5data2factor(dd,ff):
    if dd is None: return dd
    dd=float(dd)*ff
#   dd=float(format(dd,".7e")) # 8 digits
#   dd=float(format(dd,".6e")) # 7 digits
    dd=float(format(dd,".5e")) # 6 digits
    return dd

#multiply C5 error with C5 precision
def c5error2factor(dd,ff):
    if dd is None: return dd
    dd=float(dd)*ff
#   dd=float(format(dd,".7e")) # 8 digits
#   dd=float(format(dd,".6e")) # 7 digits
    dd=float(format(dd,".5e")) # 6 digits
    if dd<0: dd=-dd
    return dd

#-------------------------------------------------------------------------------
def main():
    print('Program: x4subr.py')
    print('===Self-tests===')
    rr=8.18221
    rr=8.1822124318237305
    ff=1e6
#   rr=0.1; rr=rr+0.2
#   rr=64.0; rr=rr*0.09; ff=1e-3
#   rr=1.4640001; ff=1
#   rr=1.5167123; ff=1
    dd=rr*ff
    c5=c5data2factor(rr,ff)
    print('---rr='+str(rr).ljust(21)+' ff='+str(ff).ljust(10)+' dd='+str(dd).ljust(21)+' c5='+str(c5))
#---version-0: # 8 digits
    #---rr=8.18221243182373      ff=1000000.0  dd=8182212.4318237305    c5=8182212.4
    #---rr=0.30000000000000004   ff=1000000.0  dd=300000.00000000006    c5=300000.0
    #---rr=5.76                  ff=0.001      dd=0.0057599999999999995 c5=0.00576
#---version-1: # 6 digits
    #---rr=8.18221243182373      ff=1000000.0  dd=8182212.4318237305    c5=8182210.0
    #---rr=1.5167123             ff=1          dd=1.5167123             c5=1.51671
    print('Program x4subr.py completed.')
    return

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
