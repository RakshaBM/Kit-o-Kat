import http.client
import json
import time
from pprint import pprint

import requests
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask import session

global userId, username, domain
global y, s, x

app = Flask(__name__)
app.secret_key = 'any random string'

conn = http.client.HTTPConnection("razorthinkuniversity.kickassteam.biz")

token = 'null'



@app.route('/login', methods=['POST', 'GET'])
def login():
    global domain
    # session["__invalidate__"] = True
    global s
    

    domain = request.form['domain']
    global username
    username = session['username'] = request.form['username']
    if username == session['username']:
        pprint("hellooooooooooooooo")
    password = request.form['password']
    headers = {
        'x-auth-password': "%s" % (password),
        'x-auth-domain': "%s" % (domain),
        'x-auth-username': "%s" % (username),
        'cache-control': "no-cache",
    }

    conn.request("POST", "/rest/user/login", headers=headers)
    global token, userId
    res = conn.getresponse()
    data = res.read()
    p = data.decode("utf-8")
    # print(p)
    # print(res.headers)
    if 'Ok' in p:
        token = "7882be71-53bd-429e-bb6c-8bd983323d8a"
        return redirect(url_for('getAllCompanyUsers', username=username))
    else:
        return render_template('login_error.html')


@app.route('/getAllCompanyUsers/<username>')
def getAllCompanyUsers(username):
    header = {
        'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a",
        'content-type': "application/json"
    }
    conn.request("GET", "/rest/user/getAllCompanyUsers", headers=header)
    res = conn.getresponse()
    data = res.read()
    p = data.decode("utf-8")
    j = json.loads(p)
    j1 = j['entity']
    global userId, y, s, df
    pprint(j1)
    y = []
    userId = []
    xx = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    s = []
    for index in range(len(j1)):
        j2 = j1[index]
        if (j2['status'] == 'activated'):
            s.append(index)
            y.append(j2['fname'])
            userId.append(j2['userId'])
            if username == j2['emailId']:
                df = j2['userId']
    # render_template('single.html', n=y, u=userId, ar=xx, s=s)

    return redirect(url_for('dashboardTasks'), )


# day=0 week=1
# 1-not started, 2=completed, 3=inprogress, 4=on hold, 5=stuck 6=completion rate 7=max 8=estimated hours 9=duedate


@app.route('/dashboardTasks', methods=['POST', 'GET'])
def dashboardTasks():
    if username == session['username']:
        if request.args.get('userid') == None:
            id = df
        else:
            id = request.args.get('userid')
        i = 2
        pprint("id")
        pprint(id)
        global x
        x = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        while (i >= 0):
            a = datef(i)
            ed = a[1]
            sd = a[0]
            if i == 2:
                sd = "2016-12-01"
                a = datef(1)
                ed = a[1]
                pprint(ed)

            payload = "{\n\t\"endDate\" : \"%s\",\n\t\"offsetHour\":\"5\",\n\t\"isReport\":\"true\",\n\t\"offsetMinute\" : \"30\",\n\t\"reportEndDate\" : \"%s\",\n\t\"reportStartDate\" : \"%s\",\n\t\"startDate\":\"%s\",\n\t\"userId\" : \"%s\"\n}" % (
            ed, ed, sd, sd, id)
            headers = {
                'content-type': "application/json",
                'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a"
            }
            conn.request("POST", "/rest/dashboard/dashboardTasks", payload, headers)
            res = conn.getresponse()
            data = res.read()
            h = data.decode("utf-8")
            l = json.loads(h)
            if (l['status'] == 400):
                i -= 1
                pprint(i)
                pprint("Null error")
                return render_template('single.html', n=y, u=userId, ar=x, s=s, dn=domain)
            else:
                k = l['entity']
                ''' pprint("else part")
                pprint(i)'''
                if i == 2:
                    x = dueD(k)
                    '''pprint("after due")
                    pprint(x[1][9])'''
                else:
                    x = calc(k, i)
                    '''pprint("dfdsfdfdaf")
                    pprint(x[0][9])
                    pprint(x[1][9])'''
            i -= 1
        return render_template('single.html', n=y, u=userId, ar=x, s=s, dn=domain)
    else:
        return render_template('login.html')


def datef(flag):
    from datetime import datetime, timedelta
    today = datetime.now()
    if (flag == 0):
        date_N_days_ago = datetime.now() - timedelta(days=1)
    elif (flag == 1):
        date_N_days_ago = datetime.now() - timedelta(days=7)
    elif (flag == 2):
        date_N_days_ago = datetime.now() + timedelta(days=7)
        year, month, day = today.strftime("%Y,%m,%d").split(',')
        # print(year, month, day)
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
    elif (flag == 3):
        # date_N_days_ago = datetime.now() + timedelta(days=1)
        year, month, day = today.strftime("%Y,%m,%d").split(',')
        # print(year, month, day)
        dt = datetime(int(year), int(month), int(day), 0, 0)
        s = time.mktime(dt.timetuple())
        a = int(s)
        f = []
        f.append(a * 1000)
        year, month, day = today.strftime("%Y,%m,%d").split(',')
        dt = datetime(int(year), int(month), int(day), 23, 59)
        s = time.mktime(dt.timetuple())
        a = int(s)
        f.append(a * 1000)
        return f
    date1, time1 = str(date_N_days_ago).split(' ')
    date2, time2 = str(today).split(' ')
    x = []
    x.append(date1)
    x.append(date2)
    return x


def calc(k, i):
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
    # pprint("calc end")

    return x


def dueD(k):
    a = k['taskPropertyBean']
    c = ct = 0  # c stores tasks that are due today, ct stores tasks that are due this week
    pprint("hello in dueD")
    # pprint(range(len(a)))
    # x[0][9]=x[1][9]=0
    for index in range(len(a)):
        j2 = a[index]
        d = datef(2)
        d7 = d[1]
        dd = j2['dueDate']
        d = datef(3)
        d0 = d[0]
        d1 = d[1]
        if dd <= d7:
            if dd >= d0:  # condition for week's due dates
                pprint("inside the double ifs")
                c += 1
                pprint(c)
                pprint(j2['title'])
        if dd <= d1:
            if dd >= d0:
                pprint("ct")
                ct += 1
                pprint(ct)
                pprint(j2['title'])
    # pprint(dd)
    pprint(c)
    pprint(ct)
    x[0][9] = ct
    x[1][9] = c
    return x


@app.route('/logout')
def logout():
    pprint(session['username'])
    session.pop('username', None)
    session['username'] = None

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
