from PyMusicBot import create_app
from PyMusicBot.models import db
from PyMusicBot.models.user import User


def create_admin():
    """Creates admin in the DB with 'root' login and 'toor' password"""

    app = create_app()

    with app.app_context():
        new_admin = User(name='root')
        new_admin.set_password('toor')

        db.session.add(new_admin)
        db.session.commit()


if __name__ == '__main__':
    create_admin()
