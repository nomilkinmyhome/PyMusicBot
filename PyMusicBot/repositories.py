import os

from PyMusicBot import db, logger
from PyMusicBot.models import Music

from werkzeug.utils import secure_filename, escape


class BaseRepository:
    def __init__(self):
        self.media_root: str = 'media'

    @staticmethod
    def _validate_music_title(music_title):
        if len(music_title) <= 45:
            music_title = escape(music_title)

            if not music_title.endswith('.mp3'):
                music_title: str = f'{music_title}.mp3'

            return music_title
        else:
            logger.error('The title is too long')
            raise NameError('The title is too long')

    @staticmethod
    def _get_music_from_db(music_id):
        return Music.query.filter_by(id=music_id).first()

    def save(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def edit(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class SQLAlchemyRepository(BaseRepository):
    def save(self, music_title) -> bool:
        music_title = self._validate_music_title(music_title)
        music = Music(title=music_title, path_to_file=f'{self.media_root}/{secure_filename(music_title)}')

        db.session.add(music)
        db.session.commit()

        return True

    def edit(self, music_title, music_id) -> bool:
        music_title = self._validate_music_title(music_title)
        music = self._get_music_from_db(music_id)
        music.title = music_title
        music.path_to_file = f'{self.media_root}/{secure_filename(music_title)}'

        db.session.commit()

        return True

    def delete(self, music_id) -> bool:
        music = self._get_music_from_db(music_id)

        db.session.delete(music)
        db.session.commit()

        return True


class MediaDirRepository(BaseRepository):
    def save(self, music_title, music_file) -> bool:
        if music_file is None:
            return False

        music_title = self._validate_music_title(music_title)
        music_file.save(f'{self.media_root}/{secure_filename(music_title)}')

        return True

    def edit(self, music_title, music_id) -> bool:
        music_title = self._validate_music_title(music_title)
        old_music_title = Music.query.filter(Music.id == music_id).first().title
        path_to_music = f'{self.media_root}/{secure_filename(old_music_title)}'

        if os.path.exists(path_to_music):
            os.rename(path_to_music, f'{self.media_root}/{secure_filename(music_title)}')

            return True
        else:
            return False

    def delete(self, music_id) -> bool:
        music_file = self._get_music_from_db(music_id)
        path_to_music = music_file.path_to_file

        if os.path.exists(path_to_music):
            os.remove(path_to_music)

            return True
        else:
            return False
