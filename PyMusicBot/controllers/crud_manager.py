from PyMusicBot.repositories import PostgreSQLRepository, MediaDirRepository


def save(music_title, music_file):
    MediaDirRepository().save(music_title, music_file)
    PostgreSQLRepository().save(music_title)


def edit(music_title, music_id):
    MediaDirRepository().edit(music_title, music_id)
    PostgreSQLRepository().edit(music_title, music_id)


def delete(music_id):
    MediaDirRepository().delete(music_id)
    PostgreSQLRepository().delete(music_id)
