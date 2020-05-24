from PyMusicBot import db

from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        if not password:
            raise ValueError('Password cannot be empty!')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('name')
    def validate_name(self,  key, username):
        if not username:
            raise ValueError('Username cannot be empty!')

        if len(username) > 64:
            raise ValueError('Max username length is 64 characters!')

        return username

    def __repr__(self):
        return f'<User: {self.name}; ID: {self.id}>'


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
