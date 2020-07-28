import pytest

from py_music_bot import create_app
from py_music_bot.app import login_manager
from .controllers import db, authorization


@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_mode=True)
    login_manager.init_app(app)

    with app.test_client() as test_client:
        with app.app_context():
            db.init()

        yield test_client

        db.drop()


@pytest.fixture()
def correct_auth_response(test_client):
    response = authorization.login(test_client, 'user1', 'very_bad_password')

    yield response

    authorization.logout(test_client)


@pytest.fixture()
def incorrect_auth_response(test_client):
    yield authorization.login(test_client, 'nonexistent_user', 'very_bad_password')


@pytest.fixture(scope='session')
def media_tmpdir(tmpdir_factory):
    return tmpdir_factory.mktemp('media')


@pytest.fixture(scope='session')
def music_file(media_tmpdir):
    return media_tmpdir.join('test_music.mp3')


@pytest.fixture(scope='session')
def bad_file(media_tmpdir):
    return media_tmpdir.join('bad_file.sh')
