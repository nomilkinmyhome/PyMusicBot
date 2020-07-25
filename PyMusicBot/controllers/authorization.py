from flask_login import login_user

from PyMusicBot.models.user import User


def by_login(login: str, password: str):
    user = User.query.filter_by(name=login).first()

    if not user or not user.check_password(password):
        raise ValueError('Incorrect login or password!')

    login_user(user, remember=True)
