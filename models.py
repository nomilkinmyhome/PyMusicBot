from app import db, login_manager
from datetime import datetime
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<user: {self.name}; id: {self.id}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    url = db.Column(URLType, nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Music id: {self.id}, title: {self.title}'
