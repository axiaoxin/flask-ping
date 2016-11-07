from flask_script import Manager
from extensions import app, db
from models import *  # noqa


manager = Manager(app)


@manager.command
def initdb():
    """Creates all database tables."""
    print('Database: %s' % db.engine.url)
    db.create_all()
    print('All tables created')


@manager.command
def dropdb():
    """Drops all database tables."""
    print('Database: %s' % db.engine.url)
    db.drop_all()
    print('All tables dropped')


if __name__ == "__main__":
    manager.run()
