from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Connection
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb://mongo:27017/')
db = client.todoDB
todos = db.todos

@app.route('/')
def index():
    tasks = list(todos.find())
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')
    category = request.form.get('category')

    if task:
        todos.insert_one({
            'task': task,
            'status': 'incomplete',
            'due_date': due_date,
            'priority': priority,
            'category': category
        })
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    task = request.form.get('task')
    status = request.form.get('status')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')
    category = request.form.get('category')

    todos.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'task': task,
            'status': status,
            'due_date': due_date,
            'priority': priority,
            'category': category
        }}
    )
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    todos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
