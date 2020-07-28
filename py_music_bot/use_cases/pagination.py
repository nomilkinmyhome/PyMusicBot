from flask_sqlalchemy import Pagination, BaseQuery

from py_music_bot.models.music import Music


def get_music_list(search: str) -> BaseQuery:
    if search:
        return Music.query.filter(Music.title.ilike(f'%{search}%'))

    return Music.query.order_by(Music.pub_date.desc())


def get_pages(current_page: int, search: str) -> Pagination:
    music_list: BaseQuery = get_music_list(search)

    return music_list.paginate(page=current_page, per_page=10)
