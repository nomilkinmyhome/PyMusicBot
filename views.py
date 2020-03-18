from app import app

from flask import render_template


@app.route('/')
def auth():
    context = {'page_title': 'Log in'}

    return render_template('auth.html', context=context)


@app.route('/admin')
def admin():
    context = {'page_title': 'Admin Page'}

    return render_template('admin.html', context=context)
