import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
# config


app = Flask(__name__)
app.config.from_object('_config')

# helper functions

def connect_db():
    return sqlite3.connect(app.config['DATABSE_PATH'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'loggin_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route handlers


@app.route('/logout/')
def logout():
    session.pop('loggin_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usernaem'] != app.config['USERNAME'] \
                or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['loggin_in'] = True
            flash('Welcome!')
            return redirect(url_for('task'))
        return render_template('login.html')




