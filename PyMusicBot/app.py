from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_caching import Cache

app = Flask(__name__)
app.config.from_envvar('PyMusicBot_SETTINGS')

csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
})
