from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sys, json, os

app = Flask(__name__) 

@app.route('/')
def main():
    with open('todo.json', 'r') as f:
        todos = json.load(f)
    with open('done.json', 'r') as f:
        dones = json.load(f)

    return render_template('main.html', todos=todos, dones=dones)

@app.route('/add',methods = ['GET'])
def addTodo():
    if request.method == 'GET':
        title = request.args.get('title', '')
        content = request.args.get('content', '')
        if title and content:
            with open('todo.json', 'r') as f:
                infos = json.load(f)
                info = {"id":len(infos), "title": title, "content": content, "due_date":None}
                infos.append(info)
            with open('todo.json', 'w') as f: 
                json.dump(infos, f)
        return redirect(url_for('main'))
    
@app.route('/up/<int:id>')
def up(id):
    with open('todo.json', 'r') as f:
        infos = json.load(f)
    target = infos[id]
    if id != 0:
        # switch with previous one
        prevOne = infos[id-1]
        prevOne['id'] = id
        target['id'] = id-1
        infos[id] = prevOne
        infos[id-1] = target
        with open('todo.json', 'w') as f: 
            json.dump(infos, f)
    return redirect(url_for('main'))

@app.route('/down/<int:id>')
def down(id):
    with open('todo.json', 'r') as f:
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
        with open('todo.json', 'w') as f: 
            json.dump(infos, f)
    return redirect(url_for('main'))

@app.route('/done/<int:id>')
def done(id):
    # update todo
    with open('todo.json', 'r') as f:
        infos = json.load(f)
    target = infos[id]
    del infos[id]
    newTodos = []
    for pos, info in enumerate(infos):
        newInfo = {"id":pos, "title": info['title'], "content":  info['content'], "due_date": info['due_date']}
        newTodos.append(newInfo)
    with open('todo.json', 'w') as f: 
        json.dump(newTodos, f)
    # update done
    with open('done.json', 'r') as f:
        infos = json.load(f)
    info = {"id":len(infos), "title": target['title'], "content":  target['content'], "due_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    infos.append(info)
    with open('done.json', 'w') as f: 
        json.dump(infos, f)

    return redirect(url_for('main'))


# @app.route('/edit/<int:id>')
# def edit(id):
    
# @app.route('/remove/<int:id>')
# def remove(id):
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)