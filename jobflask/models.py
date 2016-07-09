import datetime as dt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl
from passlib.hash import bcrypt_sha256 as bcrypt
import flask_login

Base = sqldcl.declarative_base ()

# Implementation parameters.
CHAR_LIMITS = {
    'abbr': 4,
    'name': 20,
}

JOB_STATES_LIST = ((1, 'new', 'Uninitialized',
                    'Created but not yet fully fleshed out'),
                   (2, 'busy', 'Busy',
                    'Currently in progress'),
                   (3, 'wait', 'Available',
                    'Available for scheduling'),
                   (4, 'idle', 'Idle',
                    'Not complete, but not ready either'),
                   (5, 'done', 'Completed',
                    'No more work to be done'),
                   (6, 'what', 'Unknown',
                    'State unknown, probably a bug'), )
JOB_STATES = dict ((jsv[0], jsv[1:])
                   for jsv in JOB_STATES_LIST)
JOB_STATES_ABBR = dict ((v[0], k)
                        for k, v in JOB_STATES.items ())

class JobOwner (Base, flask_login.UserMixin):
    """A JobOwner is a User for Flask-login credentials."""
    __tablename__ = 'users'

    id = sql.Column (sql.Integer, primary_key=True)
    name = sql.Column (sql.String (CHAR_LIMITS['name']))
    hashPass = sql.Column (sql.String (150), nullable=True)

    jobs = orm.relationship ('Job')
    events = orm.relationship ('JobLog')

    def __init__ (self, name, password):
        """Store password in a trapdoor hash."""
        self.name = name
        self.hashPass = bcrypt.encrypt (password)

    def get_id (self):
        """Return the user name for Flask-login."""
        return self.name

    def setPass (self, password):
        """Modify password, with proper hygiene."""
        self.hashPass = bcrypt.encrypt (password)

    def checkPass (self, password):
        """Test proffered password against stored hash."""
        return bcrypt.verify (password, self.hashPass)

    def __repr__ (self):
        """Display a job owner."""
        return '<JobOwner {0:d} {1:s}>'.format (self.id, self.name)

class Job (Base):
    """An individual task to be scheduled. Grist for the mill."""
    __tablename__ = 'jobs'

    id = sql.Column (sql.Integer, primary_key=True)
    name = sql.Column (sql.String (CHAR_LIMITS['name']))
    desc = sql.Column (sql.Text, nullable=True)
    state = sql.Column (sql.Enum (* (v[1] for v in JOB_STATES_LIST)),
                        default='new')

    owner = sql.Column (sql.ForeignKey ('users.id'))
    events = orm.relationship ('JobLog')

    def __repr__ (self):
        """Text representation."""
        return '<Job {0:s}>'.format (self.name)

class JobLog (Base):
    """A state change for a Job."""
    __tablename__ = 'joblog'

    id = sql.Column (sql.Integer, primary_key=True)
    timestamp = sql.Column (sql.DateTime (timezone=True),
                            default=dt.datetime.now ())
    oldState = sql.Column (sql.Enum (* (v[1] for v in JOB_STATES_LIST)))
    newState = sql.Column (sql.Enum (* (v[1] for v in JOB_STATES_LIST)))
    note = sql.Column (sql.Text, nullable=True)

    job = sql.Column (sql.ForeignKey ('jobs.id'))
    owner = sql.Column (sql.ForeignKey ('users.id'))

    def __repr__ (self):
        """Text representation."""
        return '<JobLog {0:d}>'.format (self.id)

def init_db (url, verbose=False):
    """Initialize connection to database."""
    global session
    engine = sql.create_engine (url, echo=verbose)
    session = orm.scoped_session (
        orm.sessionmaker (autocommit=False,
                          autoflush=False,
                          bind=engine))
    Base.query = session.query_property ()
    Base.metadata.create_all (bind=engine)
