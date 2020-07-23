def login(client, login, password):
    return client.post('/', data=dict(
        login=login,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)
