import string
import random

import flask
import flask_login
from . import app
from . import models

# configuration
DATABASE = 'sqlite:////tmp/jobflask.db'
SECRET_KEY = 'TYd3QTCe4pRR41F3BPrnt6XE'

# Configure JobFlask
app.config.from_object (__name__)
app.config.from_envvar ('JOBFLASK_SETTINGS', silent=True)

# Initialize the database
models.init_db  (DATABASE)

# AAA machinery
login_manager = flask_login.LoginManager ()
login_manager.init_app (app)
login_manager.login_view = 'root'

@login_manager.user_loader
def load_user (user_id):
    """Load user corresponding to ID from DB."""
    return models.session.query (models.JobOwner) \
                         .filter_by (name=user_id) \
                         .one_or_none ()

@app.teardown_appcontext
def shutdown_session (exception=None):
    models.session.remove ()

@app.route ('/')
def root ():
    """Root page: not much here."""
    return flask.render_template ('layout.html')

@app.route ('/login', methods=['POST'])
def login ():
    """Check credentials."""
    user = flask.request.form['username']
    jobo = load_user (user)
    if jobo and jobo.checkPass (flask.request.form['password']):
        flask_login.login_user (jobo)
        flask.flash ('Welcome, {0:s}'.format (user))
    else:
        flask.flash ('Invalid login attempt. Try again?')

    return flask.redirect (flask.url_for ('root'))

@app.route ('/register', methods=['POST'])
def register ():
    """Apply to register a new account."""
    # Is the account already taken?
    user = flask.request.form['email']
    if load_user (user):
        flask.flash ('That user ID is already taken, try a different one.')
        return flask.redirect (flask.url_for ('root'))

    # Generate an initial password.
    password = ''.join (random.choice (string.ascii_letters + string.digits)
                        for _ in range (24))
    print ('Temporary password for "{0:s}" is {1:s}'.format (user, password))
    flask.flash (
        'Check {0:s} for a temporary password (kidding!)'.format (user))

    # Store new user to the database
    newid = models.JobOwner (user, password)
    models.session.add (newid)
    models.session.commit ()

    # Sign in as new user
    flask_login.login_user (newid)
    return flask.render_template ('register.html')

@app.route ('/jobs', methods=['GET', 'POST'])
@flask_login.login_required
def jobs ():
    """Comprehensive job list, with optional new job."""
    if flask.request.method == 'POST':
        # Before listing jobs, make a new one
        name = flask.request.form['jobname']
        if models.session.query (models.Job) \
           .filter_by (name=name) \
           .one_or_none ():
            flask.flash ('There is already a job named {0:s}'.format (name))
        else:
            # Add new job
            newlog = models.JobLog (newState='new',
                                    owner=flask_login.current_user.id,
                                    note='Created from form')
            newjob = models.Job (name=name,
                                 desc=flask.request.form['description'],
                                 owner=flask_login.current_user.id,
                                 events=[newlog])
            models.session.add (newjob)
            models.session.commit()

    jobs = [dict (id=j.id, name=j.name, desc=j.desc, state=j.state)
            for j in models.session.query (models.Job).all ()]
    return flask.render_template ('jobs.html', jobs=jobs)

@app.route ('/onejob')
@flask_login.login_required
def onejob ():
    """Panel to edit a job."""
    error = None
    try:
        id = flask.request.args['id']
    except KeyError:
        thisJob = None
        id = None
    else:
        thisJob, owner = models.session.query (models.Job,
                                               models.JobOwner) \
                                       .filter_by (id=id) \
                                       .one_or_none ()

    if thisJob:
        states = [s[1] for s in models.JOB_STATES_LIST]
        job = dict (id=thisJob.id,
                    name=thisJob.name,
                    desc=thisJob.desc,
                    state=thisJob.state,
                    states=states,
                    owner=owner.name)
    else:
        job = None
        error = 'No job found with id {0:d}'.format (id)

    flask.flash ('Edit job: first draft')
    return flask.render_template ('onejob.html', job=job, error=error)

@app.route ('/jobEdited', methods=['POST'])
@flask_login.login_required
def jobEdited ():
    """Save result of an edit."""

    # If the user canceled edit, then don't do anything.
    action = flask.request.form.get ('submit', None)
    if action == 'Save':
        # Please continue.
        pass
    elif action == 'Cancel':
        # Ignore edit.
        flask.flash ('Not saving changes.')
        return flask.redirect (flask.url_for ('jobs'))
    else:
        # Unknown action
        flask.flash ('Unknown action {0:s}'.format (str (action)))
        return flask.redirect (flask_url_for ('jobs'))

    # Fetch the current job, if it's there
    try:
        id = int (flask.request.form['id'])
    except KeyError:
        # Form must specify a job ID
        thisJob = None
        id = None
    except ValueError:
        # Job ID must be an integer
        thisJob = None
        id = flask.request.args['id']
    else:
        # Fetch the job
        thisJob = models.session.query (models.Job) \
                  .filter_by (id=id) \
                  .one_or_none ()

    # Did the fetch work?
    if not thisJob:
        # No.
        flask.flash ('Job ID {0:s} does not exist'.format (str (id)))
    else:
        # Yes, modify the fetched job with values from the form.
        thisJob.state = flask.request.form['state']
        thisJob.desc = flask.request.form['description']
        models.session.commit ()
        flask.flash ('Job {0:d} modified'.format (id))

    return flask.redirect (flask.url_for ('jobs'))

@app.route ('/log')
@flask_login.login_required
def log ():
    """History of job activity."""
    flask.flash ('Job log: not yet implemented')
    return root ()

@app.route ('/keywords')
@flask_login.login_required
def keywords ():
    """Comprehensive job list."""
    flask.flash ('Keyword and tag management: not yet implemented')
    return root ()

@app.route ('/options')
@flask_login.login_required
def options ():
    """User option configuration."""
    flask.flash ('Option edit: not yet implemented')
    return root ()

@app.route ('/search')
@flask_login.login_required
def search ():
    """Search for jobs."""
    flask.flash ('Job search: not yet implemented')
    return root ()

@app.route ('/logout')
@flask_login.login_required
def logout ():
    flask_login.logout_user ()
    flask.flash ('You are now logged out.')
    return flask.redirect (flask.url_for ('root'))
