from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


db = SQLAlchemy()
login_manager = LoginManager()


def init_db(app):
    db.init_app(app)
    login_manager.init_app(app)


def init_manager(app):
    Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return manager


__all__ = [
    'db',
    'login_manager',
    'init_db',
    'init_manager',
]
