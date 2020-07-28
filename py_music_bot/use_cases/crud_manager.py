from py_music_bot.interactors import PostgreSQLInteractor, MediaDirInteractor


def save(music_title, music_file):
    MediaDirInteractor().save(music_title, music_file)
    PostgreSQLInteractor().save(music_title)


def edit(music_title, music_id):
    MediaDirInteractor().edit(music_title, music_id)
    PostgreSQLInteractor().edit(music_title, music_id)


def delete(music_id):
    MediaDirInteractor().delete(music_id)
    PostgreSQLInteractor().delete(music_id)
