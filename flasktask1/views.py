import sqlite3

# For store metainformation about decorated function
from functools import wraps

# Flask class, to create application
from flask import Flask

# three base tools for transaction(@app.route don't need to import)
from flask import redirect, render_template, url_for

# one tool for rapidly react
from flask import flash

#  import objects to access information
from flask import request, session, g

# from local
from forms import AddTaskForm
########################################################################

# 1. create application instance and import config
app = Flask(__name__)
app.config.from_object('_config')


# helper function to connect database
def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])


###########################################################################
# 2. log management

# 2.1 log check tools
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('GoodBye')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
           request.form['password'] != app.config['PASSWORD']:

            error = 'Invaild Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Login success!')
            return redirect(url_for('tasks'))
    else:
        return render_template('login.html')


##############################################################
# 3. tasks module

# view data
@app.route('/tasks/')
@login_required
def tasks():
    g.db = connect_db()
    cursor = g.db.execute("""
        SELECT name, due_date, priority, task_id FROM tasks where status=1
        """)
    open_tasks = [
        dict(
            name=row[0],
            due_date=row[1],
            priority=row[2],
            task_id=row[3]
            )
        for row in cursor.fetchall()
    ]
    closed_tasks = [
        dict(
            name=row[0],
            due_date=row[1],
            priority=row[2],
            task_id=row[3]
            )
        for row in cursor.fetchall()
    ]
    g.db.close()

    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
        )


# add data
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    g.db = connect_db()
    name = request.form['username']
    date = request.form['due_date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash('All fields are required. Please try again.')
        return redirect(url_for('tasks'))
    else:
        g.db.execute("""
            INSERT INTO tasks (
                name, due_date, priority, status
                )
            VALUES (
                ?, ?, ?, 1
            )
            """, [
                request.form['name'],
                request.form['due_date'],
                request.form['priority']
            ]
        )
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted.")
        return redirect(url_for('tasks'))


# modify data
@app.route('/complete/int:task_id/')
@login_required
def complete(task_id):
    g.db = connect_db()
    g.db.execute(
        'UPDATE tasks set status = 0 where task_id=' + str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was marked as complete.')
    return redirect(url_for('tasks'))


# delete data
@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute('delete from tasks where task_id=' + str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was deleted')
    return redirect(url_for('tasks'))

