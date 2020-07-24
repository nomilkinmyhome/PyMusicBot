from PyMusicBot.repositories import PostgreSqlRepository, MediaDirRepository


def save(music_title, music_file):
    MediaDirRepository().save(music_title, music_file)
    PostgreSqlRepository().save(music_title)


def edit(music_title, music_id):
    MediaDirRepository().edit(music_title, music_id)
    PostgreSqlRepository().edit(music_title, music_id)


def delete(music_id):
    MediaDirRepository().delete(music_id)
    PostgreSqlRepository().delete(music_id)
