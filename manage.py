from app import app

from app.models import db

from flask_migrate import Migrate, MigrateCommand

from flask_script import Manager

db.configure_mappers()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    """
    Drops and re-creates the SQL schema
    """
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
