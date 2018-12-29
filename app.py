from flask import Flask, render_template, request, redirect
from datetime import datetime
import json, os, pytz, pygeoip,traceback
from lib import refresh, getUserInfo, convertStringtoDate, convertDatetoString, getTextsByLang
from db import DB

app = Flask(__name__) 
gi = pygeoip.GeoIP('GeoLiteCity.dat')
db = DB()
# mode: 0 -> nothing, 1 -> edit, 2 -> add
 
@app.route('/')
def main():
    global gi, db
    # check ip
    ip = request.remote_addr
    user = getUserInfo(db, ip)
    return refresh(db, user)

@app.route('/add',methods = ['GET'])
def add():
    global db
    if request.method == 'GET':
        ip = request.remote_addr
        user = getUserInfo(db, ip)
        title = request.args.get('title', '')
        content = request.args.get('content', '')
        if title and content:
            # put new Todo at the end of list
            data = (ip, title, content,)
            db.insert_todo(data)
        # return refresh(db, user)
        return redirect('/')
    
@app.route('/up/<int:id>')
def up(id):
    global db
    ip = request.remote_addr
    user = getUserInfo(db, ip)
    if id != 0:
        # increase priority of the todo
        data = (ip, id, )
        db.increase_priority_todo(data)
        # return refresh(db, user)
        return redirect('/')

@app.route('/down/<int:id>')
def down(id):
    global db
    ip = request.remote_addr
    user = getUserInfo(db, ip)
    if id != lastNo:
        # decrease priority of the todo
        data = (ip, id, )
        db.decrease_priority_todo(data)
        # return refresh(db, user)
        return redirect('/')

@app.route('/done/<int:id>')
def done(id):
    global gi, db
    ip = request.remote_addr
    user = getUserInfo(db, ip)
    local_time = pytz.timezone(user['timezone'])
    time = datetime.utcnow().replace(microsecond=0).replace(tzinfo=pytz.utc)
    time = time.astimezone(local_time)
    data = (ip, id, time.strftime('%Y-%m-%d %H:%M:%S'))
    db.completed_todo(data)
    # return refresh(db, user)
    return redirect('/')

@app.route('/readyToAdd')
def readyToAdd():
    global gi
    ip = request.remote_addr
    data = (ip,)
    todos = db.select_todos(data)
    dones = db.select_completed_todos(data)
    data = gi.record_by_addr(ip)
    texts = getTextsByLang(data['country_name'])
    return render_template('main.html', todos=todos, dones=dones, mode=2, makeForm=True, texts=texts)

@app.route('/edit/<int:id>')
def edit(id):
    global gi, db
    ip = request.remote_addr
    data = (ip,)
    todos = db.select_todos(data)
    dones = db.select_completed_todos(data)
    data = (ip, id,)
    info = db.select_todo(data)
    # convert due_date
    if info[2] is not None:
        info[2] = convertDatetoString(info[2])
    else:
        info[2] = ''
    data = gi.record_by_addr(ip)
    texts = getTextsByLang(data['country_name'])
    return render_template('main.html', todos=todos, dones=dones, mode=1, makeForm=True, info=info, texts=texts)

@app.route('/modify/<int:id>', methods=['GET'])
def modify(id):
    global db
    if request.method == 'GET':
        ip = request.remote_addr
        user = getUserInfo(db, ip)
        title = request.args.get('title','')
        content = request.args.get('content','')
        due_date = request.args.get('due_date','')
        # convert due_date
        try:
            due_date = convertStringtoDate(due_date)
        except Exception:
            due_date = infos[id]["due_date"]
        # update target Todo
        data = (ip, id, title, content, due_date,)
        db.update_todo(data)
        # return refresh(db, user)
        return redirect('/')
    
@app.route('/remove/<int:id>')
def remove(id):
    global db
    ip = request.remote_addr
    user = getUserInfo(db, ip)
    # remove target Todo
    data = (ip, id,)
    db.remove_todo(data)
    # return refresh(db, user)
    return redirect('/')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
