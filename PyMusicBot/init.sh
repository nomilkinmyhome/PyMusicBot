if ! [ -d media/ ]
  then mkdir media
fi

if ! [ -f settings.cfg ]
  then echo -e "ENV='development'\nDEBUG=True\nSECRET_KEY=''\nMAX_CONTENT_LENGTH=32*1024*1024\nPOSTGRES_URL='127.0.0.1:5432'\nPOSTGRES_USER=''\nPOSTGRES_PW=''\nPOSTGRES_DB=''\nSQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'\nSQLALCHEMY_TRACK_MODIFICATIONS=False\n" >> settings.cfg
fi

if ! [ -f telegram_bot/.env ]
  then echo -e "TELEGRAM_BOT_TOKEN=''\nPOSTGRES_HOST='localhost'\nPOSTGRES_PORT=5432\nPOSTGRES_USER=''\nPOSTGRES_PW=''\nPOSTGRES_DB=''" >> telegram_bot/.env
fi