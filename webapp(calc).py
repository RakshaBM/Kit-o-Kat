from pprint import pprint

from flask import Flask, render_template, redirect, url_for
import http.client
import json
import datetime, timedelta
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
        if(j2['status']=='activated'):
            y.append(j2['fname'])
            userId.append(j2['userId'])

    return render_template('all_users.html', details=zip(y,userId))
#dashboardTasks accesses all the tasks of a user and calculates the necessary data

#day=0 week=1
#1-not started, 2=completed, 3=inprogress, 4=on hold, 5=stuck 6=completion rate 7=max 8=estimated hours
@app.route('/dashboardTasks',methods = ['POST', 'GET'])
def dashboardTasks():
    id=request.args.get('userid') #userid of the selected user
    i=0
    global x #x two dimensional array which stores all the data that are passed to html files
    x=[[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]
    while(i<2):
        a=datef(i)
        ed=a[1] #end date
        sd=a[0] #start date
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
        pprint("end date")
        pprint(ed)
        pprint("start date")
        pprint(sd)
        k=l['entity']
        #pprint(k)
        j=k['taskStatus']
        t=j['totalEstimationTime']
        a=0
        if 'In Progress' in j:
            x[i][3] = j['In Progress']
            a+=x[i][3]
        if 'Completed' in j:
            x[i][2] = j['Completed']
            a+=x[i][2]
        if 'On Hold' in j:
            x[i][4] = j['On Hold']
            a += x[i][4]
        if 'Stuck' in j:
            x[i][5] = j['Stuck']
            a += x[i][5]
        if 'Not Started' in j:
            x[i][1] = j['Not Started']
            a += x[i][1]
        x[i][6]=0.0
        x[i][6]=(x[i][2]/a)*100
        x[i][7]=a
        x[i][8]=(t/3600000)
        pprint(t)
        i+=1

    return render_template('graph.html', ar=x)

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
                if ((dy1 % 4 == 0 )| (dy1 % 400 == 0 & dy1 % 100 != 0)):
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
@app.route('/efficiency')
def graph():
    return render_template('efficiency.html', ar=x)
@app.route('/due')
def due():
    return render_template('due.html', ar=x)
@app.route('/taskstatus')
def taskstatus():
    return render_template('taskstatus.html', ar=x)
@app.route('/assigned')
def assigned():
    return render_template('assignedwl.html', ar=x)


if __name__ == '__main__':
   app.run(debug = True)
