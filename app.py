from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sys, json, os, pytz, pygeoip,traceback

app = Flask(__name__) 


def getLists():
    todoFileName = request.remote_addr+'_todo.json'
    doneFileName = request.remote_addr+'_done.json'
    if todoFileName not in os.listdir():
        with open(todoFileName, 'w') as f: 
            json.dump([], f)
    if doneFileName not in os.listdir():
        with open(doneFileName, 'w') as f: 
            json.dump([], f)
    with open(todoFileName, 'r') as f:
        todos = json.load(f)
    with open(doneFileName, 'r') as f:
        dones = json.load(f)
    return todos, dones

def convertStringtoDate(eng):
    month = eng[0:3]
    day = eng[4:6]
    year = eng[8:]
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    return year+'-'+months[month]+'-'+day

def convertDatetostring(d):
    d = d.split('-')
    year, month, day = d[0], d[1], d[2]
    months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    return months[month]+' '+day+', '+year

def reboot():
    todos, dones = getLists()
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    data = gi.record_by_addr(request.remote_addr)
    try:
        local_time = pytz.timezone(data['time_zone'])
    except Exception:
        local_time = pytz.timezone('Asia/Seoul')
    time = datetime.utcnow().replace(microsecond=0).replace(tzinfo=pytz.utc)
    time = time.astimezone(local_time)
    time = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
    alerts = []
    for todo in todos:
        try:
            if datetime.strptime(todo['due_date']+' 23:59:59','%Y-%m-%d %H:%M:%S') < time:
                alerts.append(todo['title'])
        except Exception:
            pass
    if alerts:
        return render_template('main.html', todos=todos, dones=dones, edit=False, alerts=alerts)
    else:
        return render_template('main.html', todos=todos, dones=dones, edit=False)

@app.route('/')
def main():
    return reboot()

@app.route('/add',methods = ['GET'])
def add():
    if request.method == 'GET':
        todoFileName = request.remote_addr+'_todo.json'
        title = request.args.get('title', '')
        content = request.args.get('content', '')
        if title and content:
            with open(todoFileName, 'r') as f:
                infos = json.load(f)
                info = {"id":len(infos), "title": title, "content": content, "due_date":None}
                infos.append(info)
            with open(todoFileName, 'w') as f: 
                json.dump(infos, f)
        return reboot()
    
@app.route('/up/<int:id>')
def up(id):
    todoFileName = request.remote_addr+'_todo.json'
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    target = infos[id]
    if id != 0:
        # switch with previous one
        prevOne = infos[id-1]
        prevOne['id'] = id
        target['id'] = id-1
        infos[id] = prevOne
        infos[id-1] = target
        with open(todoFileName, 'w') as f: 
            json.dump(infos, f)
    todos, dones = getLists()
    return render_template('main.html', todos=todos, dones=dones, edit=False)

@app.route('/down/<int:id>')
def down(id):
    todoFileName = request.remote_addr+'_todo.json'
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    lastNo = len(infos)-1
    target = infos[id]
    if id != lastNo:
        # switch with next one
        nextOne = infos[id+1]
        nextOne['id'] = id
        target['id'] = id+1
        infos[id] = nextOne
        infos[id+1] = target
        with open(todoFileName, 'w') as f: 
            json.dump(infos, f)
    todos, dones = getLists()
    return render_template('main.html', todos=todos, dones=dones, edit=False)

@app.route('/done/<int:id>')
def done(id):
    todoFileName = request.remote_addr+'_todo.json'
    doneFileName = request.remote_addr+'_done.json'
    # update todo
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    target = infos[id]
    del infos[id]
    newTodos = []
    for pos, info in enumerate(infos):
        newInfo = {"id":pos, "title": info['title'], "content":  info['content'], "due_date": info['due_date']}
        newTodos.append(newInfo)
    with open(todoFileName, 'w') as f: 
        json.dump(newTodos, f)
    # update done
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    data = gi.record_by_addr(request.remote_addr)
    local_time = pytz.timezone(data['time_zone'])
    time = datetime.utcnow().replace(microsecond=0).replace(tzinfo=pytz.utc)
    time = time.astimezone(local_time)
    with open(doneFileName, 'r') as f:
        infos = json.load(f)
    info = {"id":len(infos), "title": target['title'], "content":  target['content'], "due_date": time.strftime('%Y-%m-%d %H:%M:%S')}
    infos.append(info)
    with open(doneFileName, 'w') as f: 
        json.dump(infos, f)
    return reboot()

@app.route('/edit/<int:id>')
def edit(id):
    todoFileName = request.remote_addr+'_todo.json'
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    info = infos[id]
    if info['due_date'] is not None:
        info['due_date'] = convertDatetostring(info['due_date'])
    else:
        info['due_date'] = ''
    todos, dones = getLists()
    return render_template('main.html', todos=todos, dones=dones, edit=True, info=info)

@app.route('/modify/<int:id>', methods=['GET'])
def modify(id):
    if request.method == 'GET':
        todoFileName = request.remote_addr+'_todo.json'
        title = request.args.get('title','')
        content = request.args.get('content','')
        due_date = request.args.get('due_date','')
        with open(todoFileName, 'r') as f:
            infos = json.load(f)
        try:
            due_date = convertStringtoDate(due_date)
        except Exception:
            due_date = infos[id]["due_date"]
        infos[id] = {'id':id, "title":title, "content":content, "due_date":due_date}
        with open(todoFileName, 'w') as f: 
            json.dump(infos, f)
        return reboot()
    
@app.route('/remove/<int:id>')
def remove(id):
    # update todo
    todoFileName = request.remote_addr+'_todo.json'
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    target = infos[id]
    del infos[id]
    newTodos = []
    for pos, info in enumerate(infos):
        newInfo = {"id":pos, "title": info['title'], "content":  info['content'], "due_date": info['due_date']}
        newTodos.append(newInfo)
    with open(todoFileName, 'w') as f: 
        json.dump(newTodos, f)
    return reboot()
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)