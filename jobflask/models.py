import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl

Base = sqldcl.declarative_base ()

# Implementation parameters.
CHAR_LIMITS = {
    'abbr' : 4,
    'name' : 20,
    'desc' : 120,
}

JOB_STATES_LIST = ((1, 'new', 'Uninitialized',
                    'Created but not yet fully fleshed out' ),
                   (2, 'busy', 'Busy',
                    'Currently in progress' ),
                   (3, 'wait', 'Available',
                    'Available for scheduling' ),
                   (4, 'idle', 'Idle',
                    'Not complete, but not ready either' ),
                   (5, 'done', 'Completed',
                    'No more work to be done' ),
                   (6, 'what', 'Unknown',
                    'State unknown, probably a bug' ), )
JOB_STATES = dict ((jsv[0], jsv[1:])
                   for jsv in JOB_STATES_LIST)
JOB_STATES_ABBR = dict ((v[0], k)
                        for k, v in JOB_STATES.items ())

# We subclass User to turn it into something more flexible someday.
class JobOwner (Base):
    """This will include some more elaborate permission mechanism."""
    pass

# All models have a default ID field.

class Job (Base):
    """An individual task to be scheduled. Grist for the mill."""
    name = models.CharField (sql.String (CHAR_LIMITS['name']))
    desc = models.CharField (sql.String (CHAR_LIMITS['desc']))
    owner = models.ForeignKey (JobOwner, null=True)
    state = models.IntegerField (choices=tuple (
        (k, v[1]) for k, v in JOB_STATES.items ()))

    def __unicode__ (self):
        """Text representation."""
        return '{0:s}'.format (self.name)

class JobEventType (Base):
    """A classification of events in the Log."""
    abbrev = models.CharField (sql.String (CHAR_LIMITS['abbr']))
    name = models.CharField (sql.String (CHAR_LIMITS['name']))
    desc = models.CharField (sql.String (CHAR_LIMITS['desc']))

    def __unicode__ (self):
        """Text representation."""
        return '{0:5s} {1:s}'.format (self.abbrev, self.name)

class JobLog (Base):
    """A state change for a Job."""
    job = models.ForeignKey (Job)
    owner = models.ForeignKey (JobOwner, null=True)
    event = models.ForeignKey (JobEventType)
    timestamp = models.DateTimeField (auto_now_add=True)
    note = models.CharField (sql.String (CHAR_LIMITS['desc']))

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
