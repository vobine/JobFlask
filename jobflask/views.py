import flask
import flask_login
from . import app
from . import models 

# configuration
DATABASE = 'sqlite:////tmp/jobflask.db'

# Configure JobFlask
app.config.from_object (__name__)
app.config.from_envvar ('JOBFLASK_SETTINGS', silent=True)

# Initialize the database
models.init_db  (DATABASE)

# AAA machinery
login_manager = flask_login.LoginManager ()
login_manager.init_app (app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user (user_id):
    """With only one user, this is trivial."""
    if user_id == USERNAME:
        return User (USERNAME, PASSWORD)
    else:
        return None

@app.teardown_appcontext
def shutdown_session (exception=None):
    models.session.remove ()

@app.route ('/')
def root ():
    """Root page: not much here."""
    return flask.render_template ('layout.html')

@app.route ('/login',
            methods=['GET', 'POST'])
def login ():
    """Prompt for and check credentials."""
    return flask.render_template ('login.html')

# @flask_login.login_required
