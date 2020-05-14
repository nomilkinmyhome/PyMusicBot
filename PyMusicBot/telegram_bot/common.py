async def clear_music_title(music_title: str) -> str:
    invalid_characters: list = ['\'', '%', '/', '\\', '~', '"', '--', ';', ',', '?', '!']

    for character in invalid_characters:
        if character in music_title:
            music_title = music_title.replace(character, '')

    return music_title
