import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl

Base = sqldcl.declarative_base ()

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
