	program f00
	character*10 dat,tim
	print *,'Fortran---Hello, world---'
	call date_and_time(DATE=dat,TIME=tim)
	print *,'Fortran---Run---'
	print *,'Fortran---Date:[',dat,']'
	print *,'Fortran---Time:[',tim,']'
	stop
	end
