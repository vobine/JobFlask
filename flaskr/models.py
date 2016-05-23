import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl

Base = sqldcl.declarative_base ()

class Entries (Base):
    """FlaskR entry definition"""
    __tablename__ = 'entries'

    id = sql.Column (sql.Integer, primary_key=True)
    title = sql.Column (sql.String (80))
    text = sql.Column (sql.Text)

    def __init__ (self, title, text):
        self.title = title
        self.text = text

    def __repr__ (self):
        return '<Entry {0:d}: {1:s}>'.format (self.id, self.title)

def init_db (url='sqlite:///:memory:', verbose=False):
    """Initialize connection to database."""
    engine = sql.create_engine (url, echo=verbose)
    session = orm.scoped_session (
        orm.sessionmaker (autocommit=False,
                          autoflush=False,
                          bind=engine))
    Base.query = session.query_property ()
    Base.metadata.create_all (bind=engine)
