def login(client, login, password):
    return client.post('/', data=dict(
        login=login,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


class TestAuthPage:
    def test_is_available(self, test_client):
        response = test_client.get('/')

        assert response.status_code == 200

        assert b'PyMusicBot' in response.data
        assert b'Log in' in response.data

    def test_correct_user_auth(self, test_client, init_database):
        response = login(test_client, 'user1', 'very_bad_password')

        assert response.status_code == 200

        assert b'logout' in response.data
        assert b'Admin Page' in response.data

        logout(test_client)

    def test_incorrect_user_auth(self, test_client, init_database):
        response = login(test_client, 'nonexistent_user', 'very_bad_password')

        assert response.status_code == 200

        assert b'Incorrect login or password!' in response.data
        assert b'Admin Page' not in response.data
