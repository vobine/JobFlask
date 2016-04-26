"""ORM tutorial from SQLAlchemy.
http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
Retrieved 2016-04-23."""

import sqlalchemy as sqla
import sqlalchemy.ext.declarative as sqled

engine = sqla.create_engine ('sqlite:///:memory:', echo=True)
Base = sqled.declarative_base ()

class User (Base):
    __tablename__ = 'users'

    id = sqla.Column (sqla.Integer,
                      sqla.Sequence ('user_id_seq'),
                      primary_key=True)
    name = sqla.Column (sqla.String (50))
    fullname = sqla.Column (sqla.String (50))
    password = sqla.Column (sqla.String (12))

    def __repr__ (self):
        return "<User(name='{0:s}', fullname='{1:s}', password='{2:s}')" \
            .format (self.name, self.fullname, self.password)
