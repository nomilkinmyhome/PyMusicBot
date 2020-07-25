from flask_login import login_user

from PyMusicBot.models.user import User


def by_login(login: str, password: str) -> bool:
    user = User.query.filter_by(name=login).first()

    if user and user.check_password(password):
        login_user(user, remember=True)
        return True

    return False
