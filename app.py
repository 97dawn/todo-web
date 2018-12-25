from flask import Flask, render_template, request
from datetime import datetime
import json, os, pytz, pygeoip,traceback
from lib import reboot, getLists, convertStringtoDate, convertDatetoString, getTextsByLang

app = Flask(__name__) 
gi = pygeoip.GeoIP('GeoLiteCity.dat')
# mode: 0 -> nothing, 1 -> edit, 2 -> add
 
@app.route('/')
def main():
    return reboot(request.remote_addr)

@app.route('/add',methods = ['GET'])
def add():
    if request.method == 'GET':
        ip = request.remote_addr
        todoFileName = ip+'_todo.json'
        title = request.args.get('title', '')
        content = request.args.get('content', '')
        if title and content:
            # put new Todo at the end of list
            with open(todoFileName, 'r') as f:
                infos = json.load(f)
                info = {"id":len(infos), "title": title, "content": content, "due_date":None}
                infos.append(info)
            # save list of Todos with new Todo
            with open(todoFileName, 'w') as f: 
                json.dump(infos, f)
        return reboot(ip)
    
@app.route('/up/<int:id>')
def up(id):
    ip = request.remote_addr
    todoFileName = ip+'_todo.json'
    # get target Todo
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
    return reboot(ip)

@app.route('/down/<int:id>')
def down(id):
    ip = request.remote_addr
    todoFileName = ip+'_todo.json'
    # get target Todo
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
    return reboot(ip)

@app.route('/done/<int:id>')
def done(id):
    ip = request.remote_addr
    todoFileName = ip+'_todo.json'
    doneFileName = ip+'_done.json'
    # get target Todo
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    target = infos[id]
    # remove target Todo
    del infos[id]
    # reorder Todos
    newTodos = []
    for pos, info in enumerate(infos):
        newInfo = {"id":pos, "title": info['title'], "content":  info['content'], "due_date": info['due_date']}
        newTodos.append(newInfo)
    # update Todos
    with open(todoFileName, 'w') as f: 
        json.dump(newTodos, f)
    # update done Todo with time
    global gi
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
    return reboot(ip)

@app.route('/readyToAdd')
def readyToAdd():
    ip = request.remote_addr
    todos, dones = getLists(ip)
    global gi
    data = gi.record_by_addr(ip)
    texts = getTextsByLang(data['time_zone'])
    return render_template('main.html', todos=todos, dones=dones, mode=2, makeForm=True, texts=texts)

@app.route('/edit/<int:id>')
def edit(id):
    ip = request.remote_addr
    todoFileName = ip+'_todo.json'
    # get target Todo
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    info = infos[id]
    # convert due_date
    if info['due_date'] is not None:
        info['due_date'] = convertDatetoString(info['due_date'])
    else:
        info['due_date'] = ''
    todos, dones = getLists(ip)
    global gi
    data = gi.record_by_addr(ip)
    texts = getTextsByLang(data['time_zone'])
    return render_template('main.html', todos=todos, dones=dones, mode=1, makeForm=True, info=info, texts=texts)

@app.route('/modify/<int:id>', methods=['GET'])
def modify(id):
    if request.method == 'GET':
        ip = request.remote_addr
        todoFileName = ip+'_todo.json'
        title = request.args.get('title','')
        content = request.args.get('content','')
        due_date = request.args.get('due_date','')
        # get Todos
        with open(todoFileName, 'r') as f:
            infos = json.load(f)
        # convert due_date
        try:
            due_date = convertStringtoDate(due_date)
        except Exception:
            due_date = infos[id]["due_date"]
        # update target Todo
        infos[id] = {'id':id, "title":title, "content":content, "due_date":due_date}
        with open(todoFileName, 'w') as f: 
            json.dump(infos, f)
        return reboot(ip)
    
@app.route('/remove/<int:id>')
def remove(id):
    ip = request.remote_addr
    todoFileName = ip+'_todo.json'
    # get target Todo
    with open(todoFileName, 'r') as f:
        infos = json.load(f)
    target = infos[id]
    # remove target Todo
    del infos[id]
    # reorder Todos
    newTodos = []
    for pos, info in enumerate(infos):
        newInfo = {"id":pos, "title": info['title'], "content":  info['content'], "due_date": info['due_date']}
        newTodos.append(newInfo)
    # update Todos
    with open(todoFileName, 'w') as f: 
        json.dump(newTodos, f)
    return reboot(ip)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
