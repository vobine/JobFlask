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

class Address (Base):
    __tablename__ = 'addresses'
    id = sqla.Column (sqla.Integer, primary_key=True)
    email_address = sqla.Column (sqla.String, nullable=False)
    user_id = sqla.Column (sqla.Integer, sqla.ForeignKey ('users.id'))

    user = orm.relationship ('User', back_populates='addresses')

    def __repr__ (self):
        return 'Address (email_address="{0:s}"'.format (self.email_address)

# association table for part 3
post_keywords = sqla.Table (
    'post_keywords', Base.metadata,
    sqla.Column ('post_id',
                 sqla.ForeignKey ('posts.id'),
                 primary_key=True),
    sqla.Column ('keyword_id',
                 sqla.ForeignKey ('keywords.id'),
                 primary_key=True)
)

class BlogPost(Base):
    __tablename__ = 'posts'

    id = sqla.Column (sqla.Integer, primary_key=True)
    user_id = sqla.Column (sqla.Integer, sqla.ForeignKey('users.id'))
    headline = sqla.Column (sqla.String (255), nullable=False)
    body = sqla.Column (sqla.Text)

    # many to many BlogPost<->Keyword
    keywords = orm.relationship ('Keyword',
                                 secondary=post_keywords,
                                 back_populates='posts')

    def __init__ (self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__ (self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)

class Keyword (Base):
    __tablename__ = 'keywords'

    id = sqla.Column (sqla.Integer, primary_key=True)
    keyword = sqla.Column (sqla.String(50), nullable=False, unique=True)
    posts = orm.relationship ('BlogPost',
                              secondary=post_keywords,
                              back_populates='keywords')

    def __init__ (self, keyword):
        self.keyword = keyword

def datadef (engine, session):
    """Collect data definitions across over parts of the tutorial."""
    # Part 2: one-to-many/many-to-one mapping
    User.addresses = orm.relationship ('Address',
                                       order_by=Address.id,
                                       back_populates='user')

    # Part 3: many-to-many mapping
    BlogPost.author = orm.relationship (User, back_populates="posts")
    User.posts = orm.relationship (BlogPost, back_populates="author", lazy="dynamic")

    Base.metadata.create_all (engine)

def go_part1 (engine, session):
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

def go_part2 (engine, session):
    """Part 2: "Building a Relationship." """

    jack = User (name='jack', fullname='Jack Bean', password='Geant')
    print ("Jack's initial addresses: {0:s}".format (repr (jack.addresses)))
    jack.addresses = [ Address (email_address='jack@example.com'),
                       Address (email_address='jb25@example.com') ]
    session.add (jack)
    session.commit ()
    print ("Jack's addresses after add/commit:")
    for i, a in enumerate (jack.addresses):
        print ('{0:d} {1:s}'.format (i, repr (a)))

    for u, a in session.query (User, Address) \
                       .filter (User.id == Address.user_id) \
                       .filter (Address.email_address == 'jack@example.com') \
                       .all ():
        print ('{0:s}: {1:s}'.format (u.fullname, a.email_address))

def go_part3 (engine, session):
    """Part 3: many-to-many."""
    wendy = session.query (User) \
            .filter_by (name='wendy') \
            .one ()
    post = BlogPost ('A blog post! From Wendy! Whoa!',
                     'This is content.',
                     wendy)

    session.add (post)
    post.keywords.append (Keyword ('wendy'))
    post.keywords.append (Keyword ('first'))

    session.query (BlogPost) \
        .filter (BlogPost.keywords.any (keyword='first')) \
        .all ()
    session.query(BlogPost) \
        .filter (BlogPost.author==wendy) \
        .filter (BlogPost.keywords.any (keyword='first')) \
        .all ()
    wendy.posts \
        .filter (BlogPost.keywords.any (keyword='firstpost')) \
        .all ()


def go (hwuh='sqlite:///:memory:'):
    """Pull all of the examples together."""
    engine = sqla.create_engine (hwuh, echo=True)
    Session = orm.sessionmaker (bind=engine)
    session = Session ()

    datadef (engine, session)

    go_part1 (engine, session)
    go_part2 (engine, session)

    return dict (session=session,
                 engine=engine)
