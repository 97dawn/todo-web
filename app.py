from flask import Flask, render_template, request, redirect, url_for
import sys, json

app = Flask(__name__)

@app.route('/')
def main():
    with open('./info.json', 'r') as f:
        infos = json.load(f)
    return render_template('main.html', infos=infos)

@app.route('/add',methods = ['GET'])
def addTodo():
    if request.method == 'GET':
        title = request.args.get('title', '')
        content = request.args.get('content', '')
        with open('./info.json', 'r') as f:
            infos = json.load(f)
            info = {"id":len(infos), "title": title, "content": content, "due_date":None}
            infos.append(info)
        with open('./info.json', 'w') as f: 
            json.dump(infos, f)
        return redirect(url_for('main'))
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)