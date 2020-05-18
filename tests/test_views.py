def test_auth_page(test_client):
    response = test_client.get('/')

    assert response.status_code == 200

    assert b'PyMusicBot' in response.data
    assert b'Log in' in response.data
