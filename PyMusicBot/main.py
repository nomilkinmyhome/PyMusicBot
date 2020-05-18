from app import app
import views
from routes import init_routes


if __name__ == '__main__':
    init_routes(app)
    app.run()
