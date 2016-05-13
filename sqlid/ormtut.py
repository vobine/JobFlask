"""ORM tutorial from SQLAlchemy.
http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
Retrieved 2016-04-23."""

import sqlalchemy as sqla
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqled

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

def go (hwuh='sqlite:///:memory:'):
    """Run an example."""
    engine = sqla.create_engine (hwuh, echo=True)
    Session = orm.sessionmaker (bind=engine)
    session = Session ()

    Base.metadata.create_all (engine)

    ed_user = User (name='ed',
                    fullname='Edward L. Q. Jones',
                    password='Yeah, nope.')
    print ('Ed ID pre = {0:s}'.format (str (ed_user.id)))
    session.add (ed_user)
    print (ed_user is session.query (User).filter_by (name='ed').first ())

    session.add_all ( [
        User (name='wendy', fullname='Wendy Williams', password='still no'),
        User (name='mary', fullname='Mary Contrary', password='no grow'),
        User (name='fred', fullname='Fred Flintstone', password='rubble') ] )

    session.commit ()
    print ('Ed ID post = {0:d}'.format (ed_user.id))

    return session
