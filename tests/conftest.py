import pytest

from .db import DB
from .authorization_controller import AuthorizationController

from PyMusicBot import create_app


@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_mode=True)

    with app.test_client() as test_client:
        with app.app_context():
            DB.init()

        yield test_client

        DB.drop()


@pytest.fixture()
def correct_auth_response(test_client):
    response = AuthorizationController.login(test_client, 'user1', 'very_bad_password')

    yield response

    AuthorizationController.logout(test_client)


@pytest.fixture()
def incorrect_auth_response(test_client):
    yield AuthorizationController.login(test_client, 'nonexistent_user', 'very_bad_password')


@pytest.fixture(scope='session')
def media_tmpdir(tmpdir_factory):
    return tmpdir_factory.mktemp('media')


@pytest.fixture(scope='session')
def music_file(media_tmpdir):
    return media_tmpdir.join('test_music.mp3')


@pytest.fixture(scope='session')
def bad_file(media_tmpdir):
    return media_tmpdir.join('bad_file.sh')
