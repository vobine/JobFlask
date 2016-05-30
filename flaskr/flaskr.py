# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from . import models 
from . import app

# configuration
DATABASE = 'sqlite:////tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Initialize the database
models.init_db (DATABASE)

@app.teardown_appcontext
def shutdown_session (exception=None):
    models.session.remove ()

@app.route('/')
def show_entries():
    entries = [dict (title=u.title, text=u.text)
               for u in models.Entry.query.all ()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    models.session.add (models.Entry (title=request.form['title'],
                                     text=request.form['text']))
    models.session.commit ()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
