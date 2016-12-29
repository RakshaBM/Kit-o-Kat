def datef(flag):
    from datetime import datetime, timedelta
    t=time.time()
    N1=1
    N2=7
    d_for=datetime.now()
    dd=datetime.datetime.strptime(d_for, "%Y-%m-%d %H:%M:%S.%f")
    if(flag==1):
        d_for=datetime.now() - timedelta(days=N2)
         dd1= datetime.datetime.strptime(d_for, "%Y-%m-%d %H:%M:%S.%f")
    elif(flag==0):
        d_for=datetime.now() - timedelta(days=N1)
        dd1 = datetime.datetime.strptime(d_for, "%Y-%m-%d %H:%M:%S.%f")
    elif(flag==2):
        d_for = datetime.now() + timedelta(days=N2)
        dd1 = datetime.datetime.strptime(d_for, "%Y-%m-%d %H:%M:%S.%f")
    dt=datetime.datetime(dd.year,dd.month,dd.day,0,0)
    s=time.mktime(dt.timetuple())
    a=int(s)
    x=[]
    long_time= a*1000
    x.append(long_time)
    print(x[0])
    a=int(s)
    long_time= a*1000
    x.append(long_time)
    print(x[1])t.timetuple())
    a=int(s)
    x=[]
    long_time= a*1000
    x.append(long_time)
    print(x[0])
    a=int(s)
    long_time= a*1000
    x.append(long_time)
    print(x[1])
    if((flag==1) | (flag==2))
        temp=x[0]
        x[0]=x[1]
        x[1]=temp
    return (x)
