! ***********************************************************************************
! * Copyright (C) 2021-2022 International Atomic Energy Agency (IAEA)               *
! *-----------------------------------------------------------------------------    *
! * Permission is hereby granted, free of charge, to any person obtaining a copy    *
! * of this software and associated documentation files (the "Software"), to deal   *
! * in the Software without restriction, including without limitation the rights    *
! * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       *
! * copies of the Software, and to permit persons to whom the Software is furnished *
! * to do so, subject to the following conditions:                                  *
! *                                                                                 *
! * The above copyright notice and this permission notice shall be included in all  *
! * copies or substantial portions of the Software.                                 *
! *                                                                                 *
! * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      *
! * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        *
! * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     *
! * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          *
! * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   *
! * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN       *
! * THE SOFTWARE.                                                                   *
! *                                                                                 *
! *-----------------------------------------------------------------------------    *
! *   AUTHOR:                                                                       *
! *   Viktor Zerkin, PhD                                                            *
! *   e-mail: V.Zerkin@iaea.org                                                     *
! *   International Atomic Energy Agency                                            *
! *   Nuclear Data Section, P.O.Box 100                                             *
! *   Wagramerstrasse 5, Vienna A-1400, AUSTRIA                                     *
! *   Phone: +43 1 2600 21714; Fax: +43 1 26007                                     *
! *                                                                                 *
! ***********************************************************************************

!gfortran legrs2da.f sql1sub.c sqlite3.c -o legrs2da
!gfortran legrs2da.f sql1sub.c sqlite3.c -o legrs2da.exe -pthread -ldl
!legrs2da.exe >legrs2da.tto.txt

!____________________________________________________________________ 
!                                                                    !
	program legrs2da                                             !
!____________________________________________________________________!
	character*512  dbname
	character*512  outfile/'sql1tmp.dat'/
	character*4096 sql
	character*10 dat,tim
	character*19 datim
        write (*,*) 'Program: legrs2da.f (ver.2022-12-01)'
        write (*,*) 'Author:  V.Zerkin, IAEA-NDS, 2021-2022'
        write (*,*) 'Purpose: get LEG/RS and SIG from X4Pro;'
        write (*,*) '   calculate LEG(0) from SIG and DA from LEG(*),A;'
        write (*,*) '   output to C4: SIG(E), LEG(num), DA(A:0,180,3)'

	call date_and_time(DATE=dat,TIME=tim)
	write(datim,'(a,1h-,a,1h-,a,1h,,a,1h:,a,1h:,a)')
     1  dat(1:4),dat(5:6),dat(7:8),tim(1:2),tim(3:4),tim(5:6)
	write(*,'(a,a/)')' Running: ',datim

	dbname='../../x4sqlite1.db'

	ierr=ix4lite_open(trim(dbname)//char(0)) !--- char(0) added for compatibility with C
	if (ierr.ne.0) then
	    write (*,*) 'Cant open database'
	    stop
	endif

	write (*,*) 'Open database: ',trim(dbname),' ierr=',ierr
        write (*,*)

c	call getX4SqlSearch_LegRsSig(sql,'Cu-0','n,el')
c	call getX4SqlSearch_LegRsSig(sql,'Fe-0','n,el')
	call getX4SqlSearch_LegRsSig_debug(sql,'Cu-0','n,el')
	write (*,'(a/a)') 'SQL command:',trim(sql)

	sql=trim(sql)//char(0)
	outfile=trim(outfile)//char(0)
	call cpu_time(start)
	ipnt=ix4lite_exec(sql,outfile)
	call cpu_time(finish)
	if (ierr.lt.0) then
	    write (*,*) 'SQL error ierr=',ipnt
	else
	    write (*,*) 'Operation done successfully:',ipnt,' points'
	endif
	write(*,'(" SQL execution time: ",f6.3," sec."/)') finish-start

	call read_data(outfile,ipnt,'legrs2da.c4')
	call ix4lite_close();
	write(*,'(/a)') 'Program completed successfully'
	stop
	end


!____________________________________________________________________ 
!                                                                    !
	subroutine read_data(infile,ipnt,outfile)                    !
!____________________________________________________________________!
	character(len=*) infile,outfile
	character*132 line,nam,val,fullCode,nowTrace,lastTrace
	character*9   DatasetID
	character*4   sYear,i78,sProd,sTarg
	character*12  Author1,Author1Ini
	character*25  Refer
	character*10  Target,Projectile,Reaction
	dimension     c4data(8)
        character*9   r4tostr9
	dimension     rWnow(99)
	dimension     dWnow(99)
	character*132 c4str,c4title
	COMMON/C4OUT/ c4str,c4title
	data pi/3.14159265358979/
	i78=' '
	xx=-1.
	r4nan=sqrt(xx) ! NaN
	write (*,*) 'Read data points:',ipnt
	nin=100
	open(unit=nin,file=infile,status='old',err=9999)
	nout=101
	open(unit=nout,file=outfile,status='unknown',err=9999)
	open(unit=nout+1,file=trim(outfile)//'.zvd'
     1	,status='unknown',err=9999)
	write(nout,'(a,a,a)')
     1	'#File ',trim(outfile),' generated by program legrs2da.f'
	Enow=r4non  !!!
	dEnow=r4non !!!
	nmaxnow=-1  !!!
	lWnow=99
	iDataset=0
	iipnt=0
	lastTrace=''
	do
	    read(nin,'(a12,a)',end=8888) nam,line
	    if (nam.eq.'//EOF')       exit
	    if (nam.eq.'$DatasetID')  DatasetID=line
	    if (nam.eq.'$fullCode')   fullCode=line
	    if (nam.eq.'$YearRef1')   read(line,'(i11)') iYear
	    if (nam.eq.'$YearRef1')   sYear=line
	    if (nam.eq.'$Author1')    Author1=line
	    if (nam.eq.'$Author1Ini') Author1Ini=line
	    if (nam.eq.'$nAuthors')   read(line,'(i11)')   nAuthors
	    if (nam.eq.'$iPoint')     read(line,'(i11)')   iPoint
	    if (nam.eq.'$En')         read(line,'(e15.0)') En
	    if (nam.eq.'$dEn')        read(line,'(e15.0)') dEn
	    if (nam.eq.'$LEGRS')      read(line,'(e15.0)') rLEGRS
	    if (nam.eq.'$dLEGRS')     read(line,'(e15.0)') dLEGRS
	    if (nam.eq.'$number') then
		read(line,'(e15.0)') rnumber
		number=rnumber
	    endif
	    if (nam.eq.'$Sig')        read(line,'(e15.0)') Sig
	    if (nam.eq.'$dSig')       read(line,'(e15.0)') dSig
	    if (nam.eq.'$MF')         read(line,'(i11)')   MF
	    if (nam.eq.'$MT')         read(line,'(i11)')   MT
	    if (nam.eq.'$zaTarget1')  read(line,'(i11)') izaTarget
	    if (nam.eq.'$zaIncident1')read(line,'(i11)') izaProjectile
	    if (nam.eq.'$sTarg')      sTarg=line
	    if (nam.eq.'$sProd')      sProd=line
	    if (nam.eq.'$Target')     Target=line
	    if (nam.eq.'$Projectile') Projectile=line
	    if (nam.eq.'$Reaction')   Reaction=line
	    if (nam(1:4).eq.'####') then !--- Begin of new Datapoint
		iipnt=iipnt+1
		DatasetID=''
		fullCode=''
		iYear=0
		sYear='----'
		Author1=''
		Author1Ini=''
		nAuthors=0
		iPoint=-1
		MF=-1
		MT=-1
		izaTarget=0
		izaProjectile=0
		sTarg=''
		sProd=''
		Projectile=''
		do i=1,8
		    c4data(i)=r4nan
		enddo
		dEn=r4nan
		dLEGRS=r4nan
		dSig=r4nan
		cycle
	    endif
	    if (nam.eq.'//') then !--- End of Datapoint
		if (En.ne.Enow) then
		    call outDA(nout,Enow,nmaxnow,rWnow,dWnow)
		    Enow=En
		    dEnow=dEn
		    nmaxnow=-1
		    do i=1,lWnow
			rWnow(i)=r4nan
			dWnow(i)=r4nan
		    enddo
		endif
		write(nowTrace,*) trim(fullCode),' #',DatasetID
		if (nowTrace.ne.lastTrace) then
		    iDataset=iDataset+1
		    write(nout,'(/a,a,a,a,a,a,a,a,a,a,a,a,a)')
     1			  '#',DatasetID
     1			,' #',trim(Projectile),' #',trim(Target)
     1			,' #',sYear,',',trim(Author1Ini),trim(Author1)
     1			,' #',trim(fullCode)
		    write(c4title,'(a,a,a,a,a,a)')
     1			sYear,',',trim(Author1Ini),trim(Author1)
     1			,' #',DatasetID
		    write(nout,1001)
		    write(nout,1002)
		    write(*,*) iDataset,')---Dataset---',trim(nowTrace)
		    lastTrace=nowTrace
		endif
		write(*,*) iipnt,iPoint,' X:',En,dEn,' Y:',rLEGRS,dLEGRS
     1 		,' num:',number
		Refer=trim(Author1Ini)//trim(Author1)
!		if (nAuthors>1) Refer=trim(Refer)//',+'
		if (nAuthors>1) Refer=trim(Refer)//',et.al.'
!		Refer=trim(Refer)//'('//sYear(3:4)//')'
		Refer(22:25)='('//sYear(3:4)//')'

		c4data(1)=En
		c4data(2)=dEn
!		if (number.eq.1) then
		if (nmaxnow.lt.0) then
		    c4data(3)=Sig
		    c4data(4)=r4nan
		    if (dSig.ne.r4nan) c4data(4)=dSig
		    write(nout,1100) izaProjectile,izaTarget,sTarg
     1			,3,MT,sProd,' ',' ',(r4tostr9(c4data(i)),i=1,8)
     1			,i78,Refer,DatasetID

		    c4data(3)=Sig/(4*pi)
		    c4data(4)=r4nan
		    if (dSig.ne.r4nan) c4data(4)=dSig/(4*pi)
		    rWnow(1)=c4data(3)
		    dWnow(1)=c4data(4)
		    c4data(5)=0
		    write(nout,1100) izaProjectile,izaTarget,sTarg
     1			,MF,MT,sProd,' ',' ',(r4tostr9(c4data(i)),i=1,8)
     1			,i78,Refer,DatasetID
		endif
		c4data(3)=rLEGRS
		c4data(4)=dLEGRS
		c4data(5)=number
		rWnow(number+1)=rLEGRS
		dWnow(number+1)=dLEGRS
		nmaxnow=number
c		write(*,*) '_2_Enow:',Enow,' N:',nmaxnow
		write(nout,1100) izaProjectile,izaTarget,sTarg
     1		,MF,MT,sProd,' ',' ',(r4tostr9(c4data(i)),i=1,8)
     1		,i78,Refer,DatasetID
		write(c4str,1100) izaProjectile,izaTarget,sTarg
     1		,MF,MT,sProd,' ',' ',(r4tostr9(c4data(i)),i=1,8)
     1		,i78,Refer,DatasetID
	    endif
	enddo
	call outDA(nout,Enow,nmaxnow,rWnow,dWnow)
8888	close(nin)
	close(nout)
	call outZvdTitle(nout+1
     1	,trim(target)//'('//trim(Reaction)//')'//',DA'
     1	,'x4pro1trial: demo 2022-09-08')
	close(nout+1)
	write(*,*)'Total Datasets:',iDataset
9999	return
1100	format(I5,I6,A1,I3,I4,3A1,8A9,A3,A25,A9)
1001    format('#Proj Targ M MF MT PXC   Energy  dEnergy     Da'
     1  ,'ta   dData Cos/LO/ZP dCos/LO/AP LVL/HL dLVL/HL I78 Re'
     1  ,'fer (YY)              EntrySubP')
1002    format('#---><---->o<-><-->ooo<-------><-------><------'
     1  '-><-------><-------><-------><-------><-------><-><---'
     1  '--------------------><---><->o')
	end


!____________________________________________________________________ 
!                                                                    !
	subroutine getX4SqlSearch_LegRsSig(sql,target,react)         !
!____________________________________________________________________!
	character*4096 sql
	character(len=*) target,react
	sql=''
     1	//'select t1.Entry                            '//char(10)
     1	//' ,t1.DatasetID,t2.DatasetID as DS2         '//char(10)
     1	//' ,t1.Target,t1.Reaction                    '//char(10)
     1	//' ,t1.YearRef1,t1.nAuthors                  '//char(10)
     1	//' ,t1.Author1Ini,t1.Author1                 '//char(10)
     1	//' ,t1.fullCode,t1.iPoint                    '//char(10)
     1	//' ,t1.zaTarget1,t1.zaIncident1              '//char(10)
     1	//' ,t1.Projectile,t1.sProd,t1.sTarg          '//char(10)
     1	//' ,t2.fullCode as R2                        '//char(10)
     1	//' ,t1.MF as MF ,t1.MT as MT                 '//char(10)
     1	//' ,t2.MF as MF2,t2.MT as MT2                '//char(10)
     1	//' ,t1.y as LEGRS,t1.dy as dLEGRS            '//char(10)
     1	//' ,t2.y as Sig,t2.dy as dSig                '//char(10)
     1	//' ,t1.x1 as En,t1.dx1 as dEn,t1.dx1 as dEn2 '//char(10)
     1	//' ,t1.x2 as number                          '//char(10)
     1	//' from uni1 as t1                           '//char(10)
     1	//' inner join uni1 as t2 on t1.Entry=t2.Entry'//char(10)
     1	//'       and t1.x1=t2.x1                     '//char(10)
     1	//' where 1=1                                 '//char(10)

     1	//' and (t1.Target like '''//target//''')     '//char(10)
     1	//' and (t1.Reaction like '''//react//''')    '//char(10)
     1	//' and t1.SF58 like '',DA,,LEG/RS''          '//char(10)
     1	//' and t2.SF58 like '',SIG''                 '//char(10)
     1	//' and t2.Target=t1.Target                   '//char(10)
     1	//' and t2.Reaction=t1.Reaction               '//char(10)

c     1	//' and (t1.DatasetID=''11749005''            '//char(10)
c     1	//'   or t1.DatasetID=''40940008'')           '//char(10)
c     1	//' and (t2.DatasetID=''11749006''            '//char(10)
c     1	//'   or t2.DatasetID=''40940002'')           '//char(10)
c
c
     1	//' order by t1.fullCode,t1.YearRef1 desc     '//char(10)
     1	//' ,t1.DatasetID,En,number                   '//char(10)
	return
	end

!____________________________________________________________________ 
!                                                                    !
	subroutine getX4SqlSearch_LegRsSig_debug(sql,target,react)   !
!____________________________________________________________________!
	character*4096 sql
	character(len=*) target,react
	sql=''
     1	//'select t1.Entry                            '//char(10)
     1	//' ,t1.DatasetID,t2.DatasetID as DS2         '//char(10)
     1	//' ,t1.Target,t1.Reaction                    '//char(10)
     1	//' ,t1.YearRef1,t1.nAuthors                  '//char(10)
     1	//' ,t1.Author1Ini,t1.Author1                 '//char(10)
     1	//' ,t1.fullCode,t1.iPoint                    '//char(10)
     1	//' ,t1.zaTarget1,t1.zaIncident1              '//char(10)
     1	//' ,t1.Projectile,t1.sProd,t1.sTarg          '//char(10)
     1	//' ,t2.fullCode as R2                        '//char(10)
     1	//' ,t1.MF as MF ,t1.MT as MT                 '//char(10)
     1	//' ,t2.MF as MF2,t2.MT as MT2                '//char(10)
     1	//' ,t1.y as LEGRS,t1.dy as dLEGRS            '//char(10)
     1	//' ,t2.y as Sig,t2.dy as dSig                '//char(10)
     1	//' ,t1.x1 as En,t1.dx1 as dEn,t1.dx1 as dEn2 '//char(10)
     1	//' ,t1.x2 as number                          '//char(10)
     1	//' from uni1 as t1                           '//char(10)
     1	//' inner join uni1 as t2 on t1.Entry=t2.Entry'//char(10)
     1	//'       and t1.x1=t2.x1                     '//char(10)
     1	//' where 1=1                                 '//char(10)

c     1	//' and (t1.Target like '''//target//''')     '//char(10)
c     1	//' and (t1.Reaction like '''//react//''')    '//char(10)
c     1	//' and t1.SF58 like '',DA,,LEG/RS''          '//char(10)
c     1	//' and t2.SF58 like '',SIG''                 '//char(10)
c     1	//' and t2.Target=t1.Target                   '//char(10)
c     1	//' and t2.Reaction=t1.Reaction               '//char(10)

     1	//' and (t1.DatasetID=''11749005''            '//char(10)
     1	//'   or t1.DatasetID=''40940008'')           '//char(10)
     1	//' and (t2.DatasetID=''11749006''            '//char(10)
     1	//'   or t2.DatasetID=''40940002'')           '//char(10)

     1	//' order by t1.fullCode,t1.YearRef1 desc     '//char(10)
     1	//' ,t1.DatasetID,En,number                   '//char(10)
	return
	end


!____________________________________________________________________ 
!                                                                    !
	function r4tostr9(rr4)                                       !
!____________________________________________________________________!
!	convert real*4 to character*9
!	author:  V.Zerkin, IAEA-NDS, 2022-09-04
	character*9  r4tostr9
	character*15 c15
	r4tostr9=' '
	if (isnan(rr4)) return
	if (rr4.ge.0) then
	    write(c15,'(1p,e12.5)') rr4
	    c15=c15(2:15)
	    if (c15(10:10).eq.'0') then
	 	c15(10:14)=c15(11:15) !0
	 	c15(8:14)=c15(9:15)   !E
	    else
		write(c15,'(1p,e11.4)') rr4
		c15=c15(2:15)
	 	c15(7:14)=c15(8:15)   !E
	    endif
	else
	    write(c15,'(1p,e11.4)') rr4
	    if (c15(10:10).eq.'0') then
	 	c15(10:14)=c15(11:15) !0
	 	c15(8:14)=c15(9:15)   !E
	    else
		write(c15,'(1p,e10.3)') rr4
	 	c15(7:14)=c15(8:15)   !E
	    endif
	endif
!	write(*,*) 'r4tostr9: rr4=',rr4,' c15:[',c15,']'
	if (c15(8:9).eq.'+0') c15(8:9)='  '
	r4tostr9=c15(1:9)
	return
	end


!____________________________________________________________________ 
!                                                                    !
	subroutine outDA(nout,En,num,Wn,dWn)                         !
!____________________________________________________________________!
	dimension Wn(*)
	dimension dWn(*)
        character*9   r4tostr9
	character*20 strEn
	character*132 c4str,c4title,c4str2
	COMMON/C4OUT/ c4str,c4title
	if (isnan(En)) return
	if (num.le.0) return
	write(*,*) '___outDA:En:',En,' N:',num,' W:',(Wn(i),i=1,num+1)
c	write(strEn,'(a,''keV'')') r4tostr9(En/1e3)
c	write(strEn,'(1pe10.3,''MeV'')') En/1e6
	write(strEn,'(f8.3,''eV'')') En
	if (En.gt.1e3) write(strEn,'(f8.2,''keV'')') En/1e3
	if (En.gt.1e4) write(strEn,'(f8.1,''keV'')') En/1e3
	if (En.gt.1e5) write(strEn,'(f8.0,''keV'')') En/1e3
	if (En.gt.1e6) write(strEn,'(f8.3,''MeV'')') En/1e6
	if (En.gt.1e7) write(strEn,'(f8.2,''MeV'')') En/1e6
	do i=1,10
	    if (strEn(1:1).eq.' ') strEn(1:19)=strEn(2:20)
	enddo
	write(nout+1,'(a)') '#begin da.txt/u'
	write(nout+1,'(a,a,a,a)')'fun: ',trim(c4title),' En:',trim(strEn)
	write(nout+1,'(a)') 'con: 1'
	write(nout+1,'(a)') 'err: 3'
	write(nout+1,'(a)') 'err-fill: 6'
	write(nout+1,'(a)') '//'
c	call outDA_an(nout,En,num,Wn,dWn,1.0)
c	call outDA_an(nout,En,num,Wn,dWn,2.0)
c	call outDA_an(nout,En,num,Wn,dWn,5.0)
	do i=0,180,10
	    ang=i*1.0
	    call outDA_an(nout,En,num,Wn,dWn,ang)
	enddo
	write(nout+1,'(a)') '//'
	write(nout+1,'(a,a)') '#end da.txt/u'
	return
	end

!____________________________________________________________________ 
!                                                                    !
	subroutine outZvdTitle(nout,title,title2)                    !
!____________________________________________________________________!
        character(len=*) title,title2
	write(nout,'("#begin title/c")')
	write(nout,'(a,a)')'tit: ',trim(title)
	write(nout,'(a,a)')'tit2: ',trim(title2)
	write(nout,'("x: {|q}              ")')
	write(nout,'("x-long: Angle {|q}   ")')
	write(nout,'("x-unit: 1, (deg)     ")')
	write(nout,'("ix-unit: 1           ")')
	write(nout,'("x-units: deg         ")')
	write(nout,'("y: d{|s}/d{|W}       ")')
	write(nout,'("y-unit: 1e-3, (mb/sr)")')
	write(nout,'("iy-unit: 2           ")')
	write(nout,'("lx-win: 800")')
	write(nout,'("ly-win: 640")')
	write(nout,'("noStat: 1  ")')
	write(nout,'("buttons: 0 ")')
	write(nout,'("#end title/c")')
	return
	end

!____________________________________________________________________ 
!                                                                    !
	subroutine outDA_an(nout,En,num,W,dW,adeg)                   !
!____________________________________________________________________!
	dimension W(*)
	dimension dW(*)
	dimension P(99)
        character*9   r4tostr9
	character*132 c4str,c4title,c4str2
	COMMON/C4OUT/ c4str,c4title
	data pi/3.14159265358979/
	if (isnan(En)) return
	if (num.le.0) return
c	write(*,*) 'outDA_an:En:',En,' N:',num,' W:',(W(i),i=1,num+1)
c     1  ,' AN:',adeg  
	cosAng=cos(adeg*pi/180)
	call calcLegPol(P,cosAng,num)

	sum=1
	do i=2,num+1
	    sum=sum+W(i)*P(i)
	enddo
	f=sum*W(1)

!	https://en.wikipedia.org/wiki/Propagation_of_uncertainty
	sum=(dW(1)/W(1)*f)**2
	do i=2,num+1
	    sum=sum+(dW(i)*P(i))**2
	enddo
	df=W(1)*sqrt(sum)

c	write(*,*) 'outDA_an:En:',En,' N:',num,' W:',(W(i),i=1,num+1)
c     1  ,' AN:',adeg,' DA:',f,' dDA:',df
	write(*,*) 'outDA_an:En:',En,' ',adeg,' ',f,' ',df,df/f*100,'%'
	write(nout+1,'(f5.0,1x,g13.8,1x,g13.8)')adeg,f,df
	c4str2=c4str
	c4str2(13:15)='  4' ! MF
	c4str2(41:49)=r4tostr9(f)      ! c4data(3)
	c4str2(50:58)=r4tostr9(df)     ! c4data(4)
	c4str2(59:67)=r4tostr9(cosAng) ! c4data(5)
	c4str2(131:131)=':' ! Pointer
	write(nout,1100) c4str2
1100	format(A131)
	return
	end

!____________________________________________________________________ 
!                                                                    !
	subroutine calcLegPol(P,x,n)                                 !
!____________________________________________________________________!
!	calculate Legendre polynomials P(x,n)
	dimension P(*)
	P(1)=1.
	if (n.lt.1) return
	P(2)=x
	if (n.lt.2) return
	do L=2,n
	    P(L+1)=((2*L-1)*x*P(L) - (L-1)*P(L-1))/L
c	    write(*,*) 'calcLegPol:x:',x,' n:',n,' L:',L
c     1      ,' P(L+1):',P(L+1),' P(L):',P(L),' P(L-1):',P(L-1)
	enddo
	return
	end
