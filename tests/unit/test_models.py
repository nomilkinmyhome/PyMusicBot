import pytest

from PyMusicBot.models.user import User
from PyMusicBot.models.music import Music


class TestUserModel:
    def test_create_correct_user(self):
        user = User(name='test_user')
        user.set_password('qwerty')

        assert user.name == 'test_user'
        assert user.check_password('qwerty')
        assert repr(user) == '<User: test_user; ID: None>'

    def test_set_empty_password(self):
        with pytest.raises(ValueError) as e:
            user = User(name='test_user')
            user.set_password('')

        assert str(e.value) == 'Password cannot be empty!'

    def test_set_empty_name(self):
        with pytest.raises(ValueError) as e:
            user = User(name='')
            user.set_password('qwerty')

        assert str(e.value) == 'Username cannot be empty!'

    def test_set_long_name(self):
        with pytest.raises(ValueError) as e:
            user = User(name='a' * 65)
            user.set_password('qwerty')

        assert str(e.value) == 'Max username length is 64 characters!'


class TestMusicModel:
    def test_create_correct_music(self):
        music = Music(title='correct - name.mp3',
                      path_to_file='media/correct_-_name.mp3')

        assert music.title == 'correct - name.mp3'
        assert music.path_to_file == 'media/correct_-_name.mp3'
        assert repr(music) == '<Music ID: None, title: correct - name.mp3>'

    def test_set_empty_fields(self):
        with pytest.raises(ValueError) as e:
            music = Music(title=None, path_to_file=None)

        assert str(e.value) == 'Title cannot be empty!'

    def test_set_long_title(self):
        with pytest.raises(ValueError) as e:
            music = Music(title='a' * 60, path_to_file='media/crap')

        assert str(e.value) == 'Max title length is 45 characters!'

    def test_set_long_path(self):
        with pytest.raises(ValueError) as e:
            music = Music(title='crap', path_to_file='crap' * 50)

        assert str(e.value) == 'Max path length is 100 characters!'
