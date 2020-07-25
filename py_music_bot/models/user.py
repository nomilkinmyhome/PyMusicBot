from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


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


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
