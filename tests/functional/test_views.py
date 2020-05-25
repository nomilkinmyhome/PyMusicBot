import pytest

from .authorization_controller import AuthorizationController


class TestAuthPage:
    def test_is_available(self, test_client):
        response = test_client.get('/')

        assert response.status_code == 200

        assert b'PyMusicBot' in response.data
        assert b'Log in' in response.data

    def test_incorrect_user_auth(self, test_client):
        response = AuthorizationController.login(test_client, 'nonexistent_user', 'very_bad_password')

        assert response.status_code == 200

        assert b'Incorrect login or password!' in response.data
        assert b'Admin Page' not in response.data

    def test_correct_user_auth(self, test_client):
        response = AuthorizationController.login(test_client, 'user1', 'very_bad_password')

        assert response.status_code == 200

        assert b'logout' in response.data
        assert b'Admin Page' in response.data
        assert b'Incorrect login or password!' not in response.data


class TestAdminPagesAccess:
    _urls = ('/admin/list',
             '/admin/add',
             '/admin/edit',
             '/admin/delete')

    @pytest.mark.parametrize('url', _urls)
    def test_authorized_access(self, test_client, url):
        response = test_client.get(url)

        assert response.status_code == 200

    @pytest.mark.parametrize('url', _urls)
    def test_unautorized_access(self, test_client, url):
        AuthorizationController.logout(test_client)

        response = test_client.get(url)

        assert response.status_code == 401
