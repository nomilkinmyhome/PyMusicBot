import pytest

from PyMusicBot import create_app, db
from PyMusicBot.models import User
from PyMusicBot.routes import init_routes


def init_db():
    db.create_all()

    user1 = User(name='user1')
    user1.set_password('very_bad_password')

    db.session.add(user1)
    db.session.commit()


def drop_db():
    db.drop_all()


@pytest.fixture()
def test_client():
    app = create_app(test_mode=True)
    init_routes(app)

    with app.test_client() as test_client:
        with app.app_context():
            init_db()

        yield test_client

        drop_db()
