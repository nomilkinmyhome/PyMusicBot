from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def auth():
    return render_template('auth.html', page_title='Log in')


@app.route('/admin')
def admin():
    return render_template('admin.html', page_title='Admin Page')


if __name__ == '__main__':
    app.run()
