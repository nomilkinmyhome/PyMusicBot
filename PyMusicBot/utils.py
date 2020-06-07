import re
import os

from PyMusicBot import db
from PyMusicBot.models import Music

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename, escape


class SecureMusicCRUD:
    """CRUD secure implementation for music."""
    def __init__(self, **kwargs) -> None:
        """
        :param kwargs['music_title']: title of music

        :var self.media_root: media/ directory
        """
        self.media_root: str = 'media'

        if 'music_title' in kwargs:
            self.music_title = escape(kwargs['music_title'])
            self._get_correct_music_title()

    def _get_correct_music_title(self) -> None:
        if not self.music_title or len(self.music_title) > 45:
            self.music_title = 'Unknown - Unknown.mp3'

        if not re.search(r'^.+\.mp3$', self.music_title):
            self.music_title: str = f'{self.music_title}.mp3'

    def save_to_dir(self, music_file) -> bool:
        if music_file is None:
            return False

        music_file.save(f'{self.media_root}/{secure_filename(self.music_title)}')

        return True

    def save_to_db(self) -> bool:
        try:
            music = Music(title=self.music_title, path_to_file=f'{self.media_root}/{secure_filename(self.music_title)}')
            db.session.add(music)
            db.session.commit()

            return True
        except SQLAlchemyError:
            return False

    def rename_music_file_in_dir(self, old_music_title) -> bool:
        path_to_music = f'{self.media_root}/{secure_filename(old_music_title)}'
        if os.path.exists(path_to_music):
            os.rename(path_to_music, f'{self.media_root}/{secure_filename(self.music_title)}')

            return True
        else:
            return False

    def edit_music_in_db(self, music_id) -> bool:
        try:
            music = Music.query.filter_by(id=music_id).first()
            music.title = self.music_title
            music.path_to_file = f'{self.media_root}/{secure_filename(self.music_title)}'

            db.session.commit()

            return True
        except SQLAlchemyError:
            return False

    @staticmethod
    def delete_music_file_from_dir(music_id) -> bool:
        music = Music.query.filter_by(id=music_id).first()
        path_to_music = music.path_to_file

        if os.path.exists(path_to_music):
            os.remove(path_to_music)

            return True
        else:
            return False

    @staticmethod
    def delete_music_from_db(music_id: str) -> bool:
        try:
            music = Music.query.filter_by(id=music_id).first()

            db.session.delete(music)
            db.session.commit()

            return True
        except SQLAlchemyError:
            return False
