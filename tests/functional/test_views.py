import pytest
import io


class TestAuthPage:
    def test_is_available(self, test_client):
        response = test_client.get('/')

        assert response.status_code == 200
        assert b'PyMusicBot' in response.data
        assert b'Log in' in response.data

    def test_incorrect_user_auth(self, incorrect_auth_response):
        assert b'Incorrect login or password!' in incorrect_auth_response.data

    def test_correct_user_auth(self, correct_auth_response):
        assert b'logout' in correct_auth_response.data
        assert b'Music list' in correct_auth_response.data
        assert b'Incorrect login or password!' not in correct_auth_response.data


class TestAdminPagesAccess:
    _urls = ('/admin/list',
             '/admin/add',
             '/admin/edit',
             '/admin/delete')

    @pytest.mark.parametrize('url', _urls)
    def test_authorized_access(self, test_client, correct_auth_response, url):
        response = test_client.get(url)

        assert response.status_code == 200

    @pytest.mark.parametrize('url', _urls)
    def test_unautorized_access(self, test_client, url):
        response = test_client.get(url)

        assert response.status_code == 401


class TestAddMusicPage:
    def test_correct_upload(self, test_client, correct_auth_response, music_file):
        data = {'title': 'test - music',
                'music': (io.BytesIO(b'music'), music_file)}

        response = test_client.post('/admin/add', data=data, follow_redirects=True, content_type='multipart/form-data')

        assert b'test - music.mp3' in response.data

    def test_empty_fields(self, test_client, correct_auth_response):
        data = {'title': None,
                'music': None}

        response = test_client.post('/admin/add', data=data, follow_redirects=True, content_type='multipart/form-data')

        assert b'Music list' not in response.data
        assert b'Add music' in response.data

    def test_incorrect_title(self, test_client, correct_auth_response, music_file):
        data = {'title': 'test<> - music',
                'music': (io.BytesIO(b'music'), music_file)}

        response = test_client.post('/admin/add', data=data, follow_redirects=True, content_type='multipart/form-data')

        assert b'Music list' in response.data
        assert b'test&amp;lt;&amp;gt; - music.mp3' in response.data

    def test_incorrect_file_extension(self, test_client, correct_auth_response, bad_file):
        data = {'title': 'bad_file.sh',
                'music': (io.BytesIO(b'music'), bad_file)}

        response = test_client.post('/admin/add', data=data, follow_redirects=True, content_type='multipart/form-data')

        assert b'Music list' not in response.data
        assert b'The music file must be .mp3!' in response.data
