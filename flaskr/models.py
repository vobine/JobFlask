import sqlalchemy as sqla
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl

Base = sqldcl.declarative_base ()

class Entries (Base):
    """FlaskR entry definition"""
    __tablename__ = 'entries'

    id = sqla.Column (sqla.Integer, primary_key=True)
    title = sqla.Column (sqla.String (80))
    text = sqla.Column (sqla.Text)

    def __repr__ (self):
        return '<Entry {0:d}: {1:s}>'.format (self.id, self.title)
