import re

from app import db
from models import Music

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename, escape


class SecureMusicSave:
    """Class for secure saving music files to the DB and media/ directory"""
    def __init__(self, **kwargs) -> None:
        """:param kwargs: must contain 'music_title', 'music_file' and 'url_root'"""
        self.music_title = kwargs['music_title']
        self.music_file = kwargs['music_file']

        self.media_root: str = 'media'
        self.media_root_url: str = f'{kwargs["url_root"]}/{self.media_root}'

        self.__get_clean_music_title()
        self.__get_correct_music_title()

    def __get_clean_music_title(self) -> None:
        self.music_title: str = escape(self.music_title)
        self.music_title: str = secure_filename(self.music_title)

    def __get_correct_music_title(self) -> None:
        if not re.search(r'^.+\.mp3$', self.music_title):
            self.music_title: str = f'{self.music_title}.mp3'

    def save_to_dir(self) -> bool:
        self.music_file.save(f'{self.media_root}/{self.music_title}')

        return True

    def save_to_db(self) -> bool:
        try:
            music = Music(title=self.music_title, url=f'{self.media_root_url}{self.music_title}')
            db.session.add(music)
            db.session.commit()

            return True
        except SQLAlchemyError:
            return False
