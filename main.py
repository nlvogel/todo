from flask import render_template, url_for, redirect, request, jsonify
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from forms import AddTask
from app import app, db
import datetime as dt

with app.app_context():
    from model import *

# initialization
Bootstrap(app)
ckeditor = CKEditor(app)

# Home page, shows all tasks sorted by date ascending
@app.route('/')
def home():
    all_tasks = Task.query.all()
    # checks if any task is completed, then filters them between "to do" and "done"
    any_completed = Task.query.filter_by(completed=1).all()
    today = dt.date.today()
    return render_template('index.html', all_tasks=all_tasks, today=today, any_completed=any_completed)

# create a new task
@app.route('/add-task', methods=['GET', 'POST'])
def add_a_task():
    form = AddTask()
    if form.validate_on_submit():
        new_task = Task(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(new_task)
        db.session.commit()
        # after task is created, return to the "to do" list page
        return redirect(url_for('home'))
    return render_template('add-task.html', form=form)


# edits a task, task_id is taken from the database and applied to each task item. use wtforms for a simple form
@app.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # get the task_id from the database
    task = Task.query.get(task_id)
    # populates the data from the task in the database
    edit_form = AddTask(
        name=task.name,
        description=task.description,
        date=task.date
    )
    # updates the task if form is valid
    if edit_form.validate_on_submit():
        task.name = edit_form.name.data
        task.description = edit_form.description.data
        task.date = edit_form.date.data
        db.session.commit()
        # returns to "to do" list after task edited
        return redirect(url_for('home'))
    return render_template('add-task.html', form=edit_form, is_edit=True)


# delete a task based on task's id
@app.route('/delete-task/<int:task_id>', methods=['GET', 'POST', 'DELETE'])
def delete_task(task_id):
    # get the id of the task to be deleted
    task_to_delete = Task.query.get(task_id)
    # delete the task
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# marks a task as complete, in the code it moves to the "done" column on the homepage
@app.route('/complete-task/<int:task_id>', methods=['GET', 'POST'])
def complete_task(task_id):
    # get id of task to be completed
    task_to_complete = Task.query.get(task_id)
    # sets 'completed' to True (database takes 0 for False, 1 for True)
    task_to_complete.completed = 1
    db.session.commit()
    return redirect(url_for('home'))


# marks a task as incomplete. in the code, it moves task back to "to do" column
@app.route('/undo-complete-task/<int:task_id>', methods=['GET', 'POST'])
def undo_complete_task(task_id):
    # get id of task to mark incomplete
    task_to_undo_complete = Task.query.get(task_id)
    # sets 'completed' to False
    task_to_undo_complete.completed = 0
    db.session.commit()
    return redirect(url_for('home'))


# API
# view all tasks in json format
@app.route('/api/all-tasks')
def all_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_dict = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'date': task.date,
            'completed': task.completed
        }
        task_list.append(task_dict)
    return jsonify(task=task_list)

# runs code
if '__main__' == __name__:
    app.run(host='0.0.0.0')