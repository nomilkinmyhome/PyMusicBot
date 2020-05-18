class TestAuthPage:
    def test_is_available(self, test_client):
        response = test_client.get('/')

        assert response.status_code == 200

        assert b'PyMusicBot' in response.data
        assert b'Log in' in response.data
