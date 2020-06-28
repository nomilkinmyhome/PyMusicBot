from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_caching import Cache

import logging.config
from .config import logger_config


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(*args, **kwargs):
    app = Flask(__name__)
    app.config.from_envvar('PyMusicBot_SETTINGS')

    init_extensions(app, *args, **kwargs)

    return app


def init_extensions(app, test_mode=False):
    db.init_app(app)
    login_manager.init_app(app)

    from PyMusicBot.models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    Cache(app, config={
        'CACHE_TYPE': 'simple',
    })

    from PyMusicBot.routes import init_routes
    init_routes(app)

    if not test_mode:
        CSRFProtect(app)


app = create_app()

Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')
