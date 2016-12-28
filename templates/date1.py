def datef(flag1):
    import datetime,time
    t=time.time()
    flag=1
    d_sec= str(datetime.datetime.fromtimestamp(t))
    d_for = datetime.datetime.strptime(d_sec, "%Y-%m-%d %H:%M:%S.%f")
    dd=d_for.day
    dm=d_for.month
    dy=d_for.year
    dm1=dm
    global dd1
    global dy1
    dy1=dy
    if(flag==1):
        dd1=dd-7
    else:
        dd1=dd-1
    if(dd1==0):
        dm1=dm-1
        if(dm1==0):
            dd1=31
            dm1=12
            dy1=dy-1
        else:
            if ((dm1 == 1) | (dm1 == 3) | (dm1 == 5) | (dm1 == 7) | (dm1 == 8) | (dm1 == 10) | (dm1 == 12)):
                dd1= 31
            else:
                if (dm1 == 2):
                    a=dy1%100
                    print(a)
                    if (dy1%4==0|(dy1 % 400 == 0 &  dy1 % 100 != 0)):
                        dd1 =29
                    else:
                        dd1 =28
                else:
                    dd1 =30
    elif(dd1<0):
        dm1=dm-1
        if(dm1==0):
            dm1=12
            dy1=dy1-1
        if((dm1==1)|(dm1==3)|(dm1==5)|(dm1==7)|(dm1==8)|(dm1==10)|(dm1==12)):
                dd1=dd1+31
        elif(dm1==2):
                if (dy1 % 4 == 0 | (dy1 % 400 == 0 & dy1 % 100 != 0)):
                    dd1=dd1+29
                else:
                    dd1=dd1+28
        else:
            dd1=dd1+30
    dt=datetime.datetime(dy1,dm1,dd1,0,0)
    s=time.mktime(dt.timetuple())
    a=int(s)
    x=[]
    long_time= a*1000
    x.append(long_time)
    dt=datetime.datetime(dy,dm,dd,0,0)
    s=time.mktime(dt.timetuple())
    a=int(s)
    long_time= a*1000
    x.append(long_time)
    return (x)
