from PyMusicBot.repositories import SQLAlchemyRepository, MediaDirRepository


def save(music_title, music_file) -> bool:
    return bool(MediaDirRepository().save(music_title, music_file) and SQLAlchemyRepository().save(music_title))


def edit(music_title, music_id) -> bool:
    return bool(MediaDirRepository().edit(music_title, music_id) and SQLAlchemyRepository().edit(music_title, music_id))


def delete(music_id) -> bool:
    return bool(MediaDirRepository().delete(music_id) and SQLAlchemyRepository().delete(music_id))
