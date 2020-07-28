from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


__all__ = [
    'db',
    'init_db',
]
