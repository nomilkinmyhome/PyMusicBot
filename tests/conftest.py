import pytest

from PyMusicBot import create_app, db
from PyMusicBot.models import User
from PyMusicBot.routes import init_routes


@pytest.fixture(scope='module')
def test_app():
    app = create_app(test_mode=True)
    init_routes(app)

    ctx = app.app_context()
    ctx.push()

    yield ctx

    ctx.pop()


@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_mode=True)
    init_routes(app)

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database(test_app):
    with test_app:
        db.create_all()

    user1 = User(name='user1')
    user1.set_password('very_bad_password')

    db.session.add(user1)
    db.session.commit()

    yield db

    db.drop_all()
