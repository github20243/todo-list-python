from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=2)

    def add_task(self, task, category, priority, due_date):
        new_task = {
            "task": task,
            "category": category,
            "priority": int(priority),
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%d.%m.%Y")
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def toggle_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]["completed"] = not self.tasks[task_index]["completed"]
            self.save_tasks()

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()

todo = TodoList()

@app.route('/')
def index():
    return render_template('index.html', tasks=todo.tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    category = request.form.get('category')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    todo.add_task(task, category, priority, due_date)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    todo.toggle_task(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    todo.delete_task(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)