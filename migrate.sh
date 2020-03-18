if ! [ -d migrations/ ]; then
  PyMusicBot_SETTINGS=settings.cfg python3.8 manage.py db init
fi

PyMusicBot_SETTINGS=settings.cfg python3.8 manage.py db migrate
PyMusicBot_SETTINGS=settings.cfg python3.8 manage.py db upgrade