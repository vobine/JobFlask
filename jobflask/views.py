import flask
from . import app
from . import models 

# configuration
DATABASE = 'sqlite:////tmp/jobflask.db'

# Configure JobFlask
app.config.from_object (__name__)
app.config.from_envvar ('JOBFLASK_SETTINGS', silent=True)

# Initialize the database
models.init_db  (DATABASE)

@app.teardown_appcontext
def shutdown_session (exception=None):
    models.session.remove ()

# @app.route ('/') etc.
