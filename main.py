from flask import Flask,redirect,url_for,render_template,request, flash
from tinydb import TinyDB, Query

app=Flask(__name__)
app.config['SECRET_KEY'] = 'asecretkey!!!!'


@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        todo = request.form.get('todo')
        importance = request.form.get('importance')
        if todo != '':
            tasksDB = TinyDB('static\\task.json')
            tasksDB.insert({'id': len(tasksDB.all()), 'task':todo,  'importance':importance, 'done':False})
        else:
            flash('No Task Found!!')
        return redirect(url_for('form_submitted'))
    t = Query()
    tasks=TinyDB('static\\task.json').search(t.done==False)
    return render_template('index.html', tasks=tasks)

@app.route('/form_submitted', methods=['GET', 'POST'])
def form_submitted():
    return redirect(url_for('home'))

@app.route('/edit', methods=['POST'])
def edit1():
    if request.method=='POST':
        ide = request.form.get('taskid')
        todo = request.form.get('todo')
        importance = request.form.get('importance')
        tasks = Query()
        TinyDB("static\\task.json").update({'task':todo,  'importance':importance}, tasks.id == int(ide))
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    tasks = Query()
    task = TinyDB("static\\task.json").search(tasks.id==int(id))[0]
    return render_template('edit.html', taskedit=task)
    

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    tasks = Query()
    TinyDB("static\\task.json").update({'done': True}, tasks.id == int(id))
    return redirect(url_for('home'))



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)