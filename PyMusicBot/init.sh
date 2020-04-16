if ! [ -d media/ ]
  then mkdir media
fi

if ! [ -f settings.cfg ]
  then echo -e "ENV='development'\nDEBUG=True\n\nSECRET_KEY=''\nMAX_CONTENT_LENGTH=32*1024*1024\n\nPOSTGRES_URL='127.0.0.1:5432'\nPOSTGRES_USER='music_bot_user'\nPOSTGRES_PW='1'\nPOSTGRES_DB='music_bot'\nSQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'\nSQLALCHEMY_TRACK_MODIFICATIONS=False" >> settings.cfg
fi