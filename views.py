from app import app
from models import Music
from forms import AddMusicForm
from utils import SecureMusicSave

from flask import render_template, request, redirect, url_for
from werkzeug.exceptions import BadRequestKeyError


@app.route('/')
def auth():
    context = {'page_title': 'Log in'}

    return render_template('auth.html', context=context)


@app.route('/admin/list')
def admin_music_list():
    content_title = 'Music list'

    search = request.args.get('search')
    if search:
        music_list = Music.query.filter(Music.title.contains(search)).all()
    else:
        music_list = Music.query.order_by(Music.pub_date.desc())

    context = {'page_title': 'Admin Page',
               'content_title': content_title,
               'music_list': music_list}

    return render_template('admin.html', context=context)


@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add_music():
    if request.method == 'POST':
        try:
            music_title = request.form['title']
            music_file = request.files['music']

            secure_save = SecureMusicSave(**{'music_title': music_title,
                                             'music_file': music_file,
                                             'url_root': request.url_root})
            if secure_save.save_to_dir() and secure_save.save_to_db():
                return redirect(url_for('admin_music_list'))
        except BadRequestKeyError:
            pass

    content_title = 'Add music'

    context = {'page_title': 'Admin Page',
               'content_title': content_title,
               'add_music_form': AddMusicForm()}

    return render_template('admin.html', context=context)


@app.route('/admin/update', methods=['GET', 'POST'])
def admin_update_music():
    content_title = 'Update music'

    context = {'page_title': 'Admin Page',
               'content_title': content_title, }

    return render_template('admin.html', context=context)


@app.route('/admin/delete', methods=['GET', 'POST'])
def admin_delete_music():
    content_title = 'Delete music'

    context = {'page_title': 'Admin Page',
               'content_title': content_title, }

    return render_template('admin.html', context=context)
