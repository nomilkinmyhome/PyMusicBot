from PyMusicBot import app
import PyMusicBot.views
from PyMusicBot.routes import init_routes


if __name__ == '__main__':
    init_routes(app)
    app.run()
