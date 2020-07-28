from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from py_music_bot import app
from py_music_bot.models import db
from py_music_bot.models.user import User


def init_manager(app, db):
    Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return manager


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


manager = init_manager(app, db)


if __name__ == '__main__':
    app.run()
