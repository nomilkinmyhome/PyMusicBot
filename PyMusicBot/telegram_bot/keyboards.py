from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_with_music_list(music_list: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for music in music_list:
        keyboard.add(InlineKeyboardButton(text=music['title'], callback_data=music['path_to_file']))

    return keyboard
