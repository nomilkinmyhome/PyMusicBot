import os
import asyncpg


async def get_conn():
    return await asyncpg.connect(host=os.environ.get('POSTGRES_HOST'), port=os.environ.get('POSTGRES_PORT'),
                                 database=os.environ.get('POSTGRES_DB'),
                                 user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PW'))


async def get_music(music_title):
    conn = await get_conn()

    try:
        return await conn.fetch(f'SELECT title, path_to_file FROM music WHERE title iLIKE \'%{music_title}%\'')
    finally:
        await conn.close()
