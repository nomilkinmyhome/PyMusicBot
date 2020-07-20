if ! [ -d PyMusicBot/media/ ]
  then mkdir PyMusicBot/media
fi

if ! [ -f PyMusicBot/telegram_bot/.env ]
  then echo -e "TELEGRAM_BOT_TOKEN=''\nPOSTGRES_HOST='localhost'\nPOSTGRES_PORT=5432\nPOSTGRES_USER=''\nPOSTGRES_PW=''\nPOSTGRES_DB=''" >> PyMusicBot/telegram_bot/.env
fi