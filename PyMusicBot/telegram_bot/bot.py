import os
import sys
import logging

from dotenv import load_dotenv
from typing import Union

from aiogram import Bot, Dispatcher, executor, types

if os.path.exists('.env'):
    load_dotenv('.env')

    from PyMusicBot.telegram_bot.keyboards import get_keyboard_with_music_list
    from PyMusicBot.telegram_bot.database import get_music

    token: str = os.environ.get('TELEGRAM_BOT_TOKEN')
else:
    print('ERROR: .env file does not exist!')
    sys.exit(1)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Hello! Send me the name of the song')


@dp.message_handler()
async def get_music_title(message: types.Message):
    music_list: list = await get_music_list(message.text)

    if music_list:
        if len(music_list) == 1:
            await send_music(message.from_user.id, music_list[0]['path_to_file'])
        else:
            await message.answer('There are several similar songs. Choose the song:',
                                 reply_markup=get_keyboard_with_music_list(music_list))
    else:
        await message.answer('There is no such song in the database!')


@dp.callback_query_handler()
async def send_selected_music(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await send_music(callback_query.from_user.id, callback_query.data)


async def send_music(chat_id: str, path_to_music: str):
    try:
        music: types.InputFile = types.InputFile(f'../{path_to_music}')

        msg = await bot.send_message(chat_id, 'Sending song...')
        await bot.send_audio(chat_id, music)
        await bot.delete_message(chat_id, msg['message_id'])
    except FileNotFoundError:
        await bot.send_message(chat_id, 'Something went wrong. Please try again later')


async def get_music_list(music_title: str) -> Union[list, None]:
    music_list = await get_music(music_title)

    if not music_list:
        return None

    return music_list


if __name__ == '__main__':
    executor.start_polling(dp)
