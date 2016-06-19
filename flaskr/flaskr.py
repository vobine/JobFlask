# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from . import models 
from . import app
import flask_login as fl

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

# Flask-login machinery
class User (fl.UserMixin):
    """Flask-login user class"""

    def __init__ (self, name, password):
        """Store user credentials."""
        self._name = name
        self._password = password

    def get_id (self):
        """Is this obvious? Let me think about it...."""
        return self._name

login_manager = fl.LoginManager ()
login_manager.init_app (app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user (user_id):
    """With only one user, this is trivial."""
    if user_id == USERNAME:
        return User (USERNAME, PASSWORD)
    else:
        return None

# Flask machinery
@app.teardown_appcontext
def shutdown_session (exception=None):
    models.session.remove ()

@app.route('/')
@fl.login_required
def show_entries():
    entries = [dict (title=u.title, text=u.text)
               for u in models.Entry.query.all ()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
@fl.login_required
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
            fl.login_user (User (app.config['USERNAME'],
                                 app.config['PASSWORD']))
            flash('You were logged in')
            return redirect(url_for('show_entries'))

    return render_template('login.html', error=error)

@app.route('/logout')
@fl.login_required
def logout():
    session.pop('logged_in', None)
    fl.logout_user ()
    flash('You were logged out')
    return redirect(url_for('login'))
