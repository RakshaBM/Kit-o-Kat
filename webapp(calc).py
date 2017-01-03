from pprint import pprint

from flask import Flask, render_template, redirect, url_for
import http.client
import json
from flask import request
import time


app = Flask(__name__)

conn = http.client.HTTPConnection("razorthinkuniversity.kickassteam.biz")
token='null'

global x
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
        return redirect(url_for('getAllCompanyUsers'))
    else:
        return render_template('login_error.html')


@app.route('/getAllCompanyUsers')
def getAllCompanyUsers():
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
        if (j2['status'] == 'activated'):
            y.append(j2['fname'])
            userId.append(j2['userId'])

    return render_template('all_users.html', details=zip(y,userId))

global x
#day=0 week=1
#1-not started, 2=completed, 3=inprogress, 4=on hold, 5=stuck 6=completion rate 7=max 8=estimated hours 9=duedate
@app.route('/dashboardTasks',methods = ['POST', 'GET'])
def dashboardTasks():
    id=request.args.get('userid')
    i=2
    global x
    x=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    while(i>=0):
        a=datef(i)
        ed=a[1]
        sd=a[0]
        if i == 2:
            sd="2016-12-01"
            a=datef(1)
            ed="2016-12-28"
            pprint(ed)


        payload = "{\n\t\"endDate\" : \"%s\",\n\t\"offsetHour\":\"5\",\n\t\"isReport\":\"true\",\n\t\"offsetMinute\" : \"30\",\n\t\"reportEndDate\" : \"%s\",\n\t\"reportStartDate\" : \"%s\",\n\t\"startDate\":\"%s\",\n\t\"userId\" : \"%s\"\n}" % (ed,ed,sd,sd,id)
        headers = {
            'content-type': "application/json",
            'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a"
        }
        conn.request("POST", "/rest/dashboard/dashboardTasks", payload, headers)
        res = conn.getresponse()
        data = res.read()
        h=data.decode("utf-8")
        l = json.loads(h)
        if(l['status'] == 400):
            i -= 1
            pprint(i)
            pprint("Null error")

            '''pprint(x[0])
            pprint(x[1])'''
            return render_template('graph.html', ar=x)
        else:
            k = l['entity']
            ''' pprint("else part")
            pprint(i)'''
            if i == 2:
                x = dueD(k)
                pprint("after due")
                pprint(x[1][9])
            else:
                x = calc(k, i)
                '''pprint("dfdsfdfdaf")
                pprint(x[0][9])
                pprint(x[1][9])'''
        i -= 1
    return render_template('graph.html', ar=x)


def datef(flag):
    from datetime import datetime,timedelta
    today=datetime.now()
    if(flag==0):
        date_N_days_ago = datetime.now() - timedelta(days=1)
    elif(flag==1):
        date_N_days_ago = datetime.now() - timedelta(days=7)
    elif(flag==2):
        date_N_days_ago = datetime.now() + timedelta(days=7)
        year, month, day = today.strftime("%Y,%m,%d").split(',')
        #print(year, month, day)
        dt = datetime(int(year), int(month), int(day), 0, 0)
        s = time.mktime(dt.timetuple())
        a = int(s)
        f = []
        f.append(a * 1000)
        year, month, day = date_N_days_ago.strftime("%Y,%m,%d").split(',')
        dt = datetime(int(year), int(month), int(day), 0, 0)
        s = time.mktime(dt.timetuple())
        a = int(s)
        f.append(a * 1000)
        return f
    elif(flag==3):
        date_N_days_ago = datetime.now() + timedelta(days=1)
    date1,time1= str(date_N_days_ago).split(' ')
    date2,time2= str(today).split(' ')
    x = []
    x.append(date1)
    x.append(date2)
    if((flag==2)|(flag==3)):
        temp=x[0]
        x[0]=x[1]
        x[1]=temp
    return(x)


def calc(k,i):
    j = k['taskStatus']
    t = j['totalEstimationTime']
    a = 0
    if 'In Progress' in j:
        x[i][3] = j['In Progress']
        a += x[i][3]
    if 'Completed' in j:
        x[i][2] = j['Completed']
        a += x[i][2]
    if 'On Hold' in j:
        x[i][4] = j['On Hold']
        a += x[i][4]
    if 'Stuck' in j:
        x[i][5] = j['Stuck']
        a += x[i][5]
    if 'Not Started' in j:
        x[i][1] = j['Not Started']
        a += x[i][1]
    x[i][6] = 0.0
    x[i][6] = (x[i][2] / a) * 100
    x[i][7] = a
    x[i][8] = (t / 3600000)
    #pprint("calc end")

    return x


def dueD(k):
    a = k['taskPropertyBean']
    c = ct = 0 # c stores tasks that are due today, ct stores tasks that are due this week
    pprint("hello in dueD")
    # pprint(range(len(a)))
    x[0][9]=x[1][9]=0
    for index in range(len(a)):
        j2 = a[index]
        d = datef(2)
        d7 = d[1]
        d0 = d[0]
        dd=j2['dueDate']
        #pprint(dd)
        if dd <= d7 & dd >= d0: # condition for week's due dates
            c += 1
            pprint("today")
            pprint(j2['title'])
       # pprint("one if done")
        if dd == d0:
            ct += 1
            pprint("week")
            pprint(j2['title'])
    #pprint(dd)
    pprint(d7)
    pprint(d0)
    x[0][9] = c
    x[1][9] = ct
    pprint("dueD")
    pprint(x[0][9])
    pprint(x[1][9])
    pprint("dueD end")
    return x


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
