import re

from app import db
from models import Music
from sqlalchemy.exc import SQLAlchemyError

from werkzeug.utils import secure_filename, escape


class SecureMusicSave:
    def __init__(self, **kwargs):
        self.music_title = kwargs['music_title']
        self.music_file = kwargs['music_file']

        self.media_root = 'media'
        self.media_root_url = f'{kwargs["url_root"]}/{self.media_root}'

        self.__get_clean_music_title()

    def __get_clean_music_title(self):
        if not re.search(r'^.+\.mp3$', self.music_title):
            self.music_title = f'{self.music_title}.mp3'
        self.music_title = escape(self.music_title)
        self.music_title = secure_filename(self.music_title)

    def save_to_dir(self):
        self.music_file.save(f'{self.media_root}/{self.music_title}')

        return True

    def save_to_db(self):
        try:
            music = Music(title=self.music_title, url=f'{self.media_root_url}{self.music_title}')
            db.session.add(music)
            db.session.commit()

            return True
        except SQLAlchemyError:
            return False
