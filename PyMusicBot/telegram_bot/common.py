async def clear_music_title(music_title):
    invalid_characters = ['\'', '%', '/', '\\', '~', '"', '--', ';', ',', '?', '!']

    for character in invalid_characters:
        if character in music_title:
            music_title = music_title.replace(character, '')

    return music_title
