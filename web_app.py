from pprint import pprint

from flask import Flask, render_template, redirect, url_for
import http.client
import json

from flask import request
from pip._vendor import requests

app = Flask(__name__)

conn = http.client.HTTPConnection("razorthinkuniversity.kickassteam.biz")
token='null'

@app.route('/login',methods = ['POST', 'GET'])
def login():
    domain = request.form['domain']
    username = request.form['username']
    password = request.form['password']
    if ("%s" %(username)=="karthik.b@razorthink.net"):
        headers = {
            'x-auth-password': "%s" % (password),
            'x-auth-domain': "%s" % (domain),
            'x-auth-username': "%s" % (username),
            'cache-control': "no-cache",
        }
    else:
        return render_template('login_error.html')
        

    conn.request("POST", "/rest/user/login", headers=headers)
    global token
    res = conn.getresponse()
    data = res.read()
    p = data.decode("utf-8")
    print(p)
    print(res.headers)
    if 'Ok' in p:
        token = res.headers['x-auth-token']
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
        'x-auth-token': "%s" % (new_token),
        'content-type': "application/json"
    }
    conn.request("GET", "/rest/user/getAllCompanyUsers", headers=header)
    res = conn.getresponse()
    data = res.read()
    p = data.decode("utf-8")
    j = json.loads(p)
    j1= j['entity']
    x = []
    for index in range(len(j1)):
        j2 = j1[index]
        x.append(j2['fname'])

    pprint(j)
    return render_template('all_users.html', fullname=x)



@app.route('/getTasks')
def getTasks():
    payload = "{\n\"offsetHour\": \"5\",\n\"offsetMinute\": \"30\",\n\"pageNumber\": \"0\",\n\"pageSize\": \"6\",\n\"status\": \"1\",\n\"workstreamId\": \"1038\"\n            }\n\n"

    headers = {
        'content-type': "application/json",
        'x-auth-token': "7882be71-53bd-429e-bb6c-8bd983323d8a"
    }

    conn.request("POST", "/rest/task/getTasks", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return (data.decode("utf-8"))


if __name__ == '__main__':
   app.run(debug = True)
