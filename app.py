from flask import Flask
from flask import render_template

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def auth():
    return render_template('auth.html', page_title='Log in')


@app.route('/admin')
def admin():
    return 'None'


if __name__ == '__main__':
    app.run()
