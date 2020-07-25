"""This module contains all project repositories: PsotgreSQLRepository and MediaDirRepository"""

import os

from werkzeug.utils import secure_filename, escape

from py_music_bot.models import db
from py_music_bot.models.music import Music


class BaseRepository:
    """Base class for all repositories"""

    def __init__(self):
        self.media_root: str = 'media'

    @staticmethod
    def _validate_music_title(music_title):
        """Validates music title.

        Max title length - 45 symbols.
        Title must be .mp3"""

        if len(music_title) <= 45:
            music_title = escape(music_title)

            if not music_title.endswith('.mp3'):
                music_title: str = f'{music_title}.mp3'

            return music_title
        else:
            raise ValueError('The title is too long')

    @staticmethod
    def _get_music_from_db(music_id):
        return Music.query.filter_by(id=music_id).first()

    def save(self, *args, **kwargs):
        raise NotImplementedError

    def edit(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class PostgreSQLRepository(BaseRepository):
    """Database repository"""

    def save(self, music_title):
        music_title = self._validate_music_title(music_title)
        music = Music(title=music_title, path_to_file=f'{self.media_root}/{secure_filename(music_title)}')

        db.session.add(music)
        db.session.commit()

    def edit(self, music_title, music_id):
        music_title = self._validate_music_title(music_title)
        music = self._get_music_from_db(music_id)
        music.title = music_title
        music.path_to_file = f'{self.media_root}/{secure_filename(music_title)}'

        db.session.commit()

    def delete(self, music_id):
        music = self._get_music_from_db(music_id)

        db.session.delete(music)
        db.session.commit()


class MediaDirRepository(BaseRepository):
    """Media directory repository"""

    def save(self, music_title, music_file):
        music_title = self._validate_music_title(music_title)
        music_file.save(f'{self.media_root}/{secure_filename(music_title)}')

    def edit(self, music_title, music_id):
        music_title = self._validate_music_title(music_title)
        old_music_title = Music.query.filter(Music.id == music_id).first().title
        path_to_music = f'{self.media_root}/{secure_filename(old_music_title)}'

        if not os.path.exists(path_to_music):
            raise FileNotFoundError

        os.rename(path_to_music, f'{self.media_root}/{secure_filename(music_title)}')

    def delete(self, music_id):
        music_file = self._get_music_from_db(music_id)
        path_to_music = music_file.path_to_file

        if not os.path.exists(path_to_music):
            raise FileNotFoundError

        os.remove(path_to_music)
