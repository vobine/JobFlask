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

def go_part1 (engine, session, hwuh='sqlite:///:memory:'):
    """Run an example."""
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

class Address (Base):
    __tablename__ = 'addresses'
    id = sqla.Column (sqla.Integer, primary_key=True)
    email_address = sqla.Column (sqla.String, nullable=False)
    user_id = sqla.Column (sqla.Integer, sqla.ForeignKey ('users.id'))

    user = orm.relationship ('User', back_populates='addresses')

    def __repr__ (self):
        return 'Address (email_address="{0:s}"'.format (self.email_address)

def go_part2 (engine, session, huwh='sqlite:///:memory:'):
    """Part 2: "Building a Relationship." """
    User.addresses = orm.relationship ('Address',
                                       order_by=Address.id,
                                       back_populates='user')
    Base.metadata.create_all (engine)

    jack = User (name='jack', fullname='Jack Bean', password='Geant')
    print ("Jack's initial addresses: {0:s}".format (repr (jack.addresses)))
    jack.addresses = [ Address (email_address='jack@example.com'),
                       Address (email_address='jb25@example.com') ]
    session.add (jack)
    session.commit ()
    print ("Jack's addresses after add/commit:")
    for i, a in enumerate (jack.addresses):
        print ('{0:d} {1:s}'.format (i, repr (a)))

def go (hwuh='sqlite:///:memory:'):
    """Pull all of the examples together."""
    engine = sqla.create_engine (hwuh, echo=True)
    Session = orm.sessionmaker (bind=engine)
    session = Session ()

    Base.metadata.create_all (engine)

    go_part1 (engine, session, hwuh)
    # go_part2 (engine, session, hwuh)

    return dict (session=session,
                 engine=engine)
