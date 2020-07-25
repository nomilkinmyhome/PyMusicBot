from datetime import datetime

from sqlalchemy.orm import validates

from . import db


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    path_to_file = db.Column(db.String(100), nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.now)

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title cannot be empty!')

        if len(title) > 45:
            raise ValueError('Max title length is 45 characters!')

        return title

    @validates('path_to_file')
    def validate_path_to_file(self, key, path_to_file):
        if not path_to_file:
            raise ValueError('Path cannot be empty!')

        if len(path_to_file) > 100:
            raise ValueError('Max path length is 100 characters!')

        return path_to_file

    def __repr__(self):
        return f'<Music ID: {self.id}, title: {self.title}>'
