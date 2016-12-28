from pprint import pprint

from flask import Flask, render_template, redirect, url_for
import http.client
import json

from flask import request


app = Flask(__name__)

conn = http.client.HTTPConnection("razorthinkuniversity.kickassteam.biz")
token='null'

@app.route('/login',methods = ['POST', 'GET'])
def login():
    domain = request.form['domain']
    username = request.form['username']
    password = request.form['password']
    headers = {
            'x-auth-password': "%s" % (password),
            'x-auth-domain': "%s" % (domain),
            'x-auth-username': "%s" % (username),
            'cache-control': "no-cache",
    }

    conn.request("POST", "/rest/user/login", headers=headers)
    global token
    res = conn.getresponse()
    data = res.read()
    p = data.decode("utf-8")
    #print(p)
    #print(res.headers)
    if 'Ok' in p:
        token = "7882be71-53bd-429e-bb6c-8bd983323d8a"
        return redirect(url_for('getAllCompanyUsers', new_token=token))
    else:
        return render_template('login_error.html')




@app.route('/getLoggedInUser')
def authen():
   # username = request.form['username']
    #password = request.form['password']
   # domain = request.form['domain']
    header = {
        'content-type': "application/json",
        'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a"
    }
    conn.request("GET", "/rest/user/getLoggedInUser", headers=header)
    res = conn.getresponse()
    data = res.read()
    return (data)


@app.route('/work_stream')
def work_stream():
    header = {
        'content-type': "application/json",
        'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a"
    }
    conn.request("GET", "/rest/workstream/getWorkStream", headers=header)
    res = conn.getresponse()
    data = res.read()
    return (data)


@app.route('/getAllCompanyUsers/<new_token>')
def getAllCompanyUsers(new_token):
    header = {
        'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a",
        'content-type': "application/json"
    }
    conn.request("GET", "/rest/user/getAllCompanyUsers", headers=header)
    res = conn.getresponse()
    data = res.read()
    p = data.decode("utf-8")
    j = json.loads(p)
    j1= j['entity']
    y = []
    userId = []
    for index in range(len(j1)):
        j2 = j1[index]
        y.append(j2['fname'])
        userId.append(j2['userId'])

    pprint(j)
    return render_template('all_users.html', details=zip(y,userId))


#day=0 week=1
#1-not started, 2=completed, 3=inprogress, 4=on hold, 5=stuck
@app.route('/dashboardTasks',methods = ['POST', 'GET'])
def dashboardTasks():
    id=request.args.get('userid')
    i=0
    x=[[0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    while(i<2):
        a=datef(i)
        ed=a[1]
        sd=a[0]

        pprint(i)
        payload = "{\n\t\"endDate\" : \"%s\",\n\t\"offsetHour\":\"5\",\n\t\"isReport\":\"true\",\n\t\"offsetMinute\" : \"30\",\n\t\"pageNumber\" : \"0\",\n\t\"pageSize\" : \"5\",\n\t\"startDate\":\"%s\",\n\t\"userId\" : \"%s\"\n}" % (ed,sd,id)
        headers = {
            'content-type': "application/json",
            'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a"
        }
        conn.request("POST", "/rest/dashboard/dashboardTasks", payload, headers)

        res = conn.getresponse()
        data = res.read()
        h=data.decode("utf-8")
        l = json.loads(h)
        #pprint(l)
        k=l['entity']
        #pprint(k)
        j=k['taskStatus']
       # pprint(j)

        if 'In Progress' in j:
            x[i][3] = j['In Progress']

        if 'Completed' in j:
            x[i][2] = j['Completed']

        if 'On Hold' in j:
            x[i][4] = j['On Hold']

        if 'Stuck' in j:
            x[i][5] = j['Stuck']

        if 'Not Started' in j:
            x[i][1] = j['Not Started']
        i+=1
        pprint(ed)
        pprint(sd)
        #pprint("array")
        #pprint(x[1][5])
    return render_template('tasks.html', ar=x)
def datef(flag):
    import datetime,time
    t=time.time()
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
        dd1=dd+1
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

if __name__ == '__main__':
   app.run(debug = True)
