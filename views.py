from app import app
from models import Music
from forms import AddMusicForm, EditMusicForm, DeleteMusicForm, AuthForm
from utils import SecureMusicCRUD

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from models import User
from werkzeug.exceptions import BadRequestKeyError


@app.route('/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['login']).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user, remember=True)
            return redirect(url_for('admin_music_list'))

    if current_user.is_authenticated:
        return redirect(url_for('admin_music_list'))

    context = {'page_title': 'Log in',
               'auth_form': AuthForm()}

    return render_template('auth.html', context=context)


@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))


@app.route('/admin/list')
@login_required
def admin_music_list():
    content_title = 'Music list'

    current_page = request.args.get('page')
    if current_page and current_page.isdigit():
        current_page = int(current_page)
    else:
        current_page = 1

    search = request.args.get('search')
    if search:
        music_list = Music.query.filter(Music.title.ilike(f'%{search}%'))
    else:
        music_list = Music.query.order_by(Music.pub_date.desc())

    pages = music_list.paginate(page=current_page, per_page=10)

    context = {'page_title': 'Admin Page',
               'content_title': content_title,
               'search': search,
               'pages': pages}

    return render_template('admin.html', context=context)


@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def admin_add_music():
    if request.method == 'POST':
        try:
            music_title = request.form['title']
            music_file = request.files['music']

            secure_save = SecureMusicCRUD(**{'music_title': music_title,
                                             'url_root': request.url_root})
            if secure_save.save_to_dir(music_file) and secure_save.save_to_db():
                return redirect(url_for('admin_music_list'))
        except BadRequestKeyError:
            pass

    content_title = 'Add music'

    context = {'page_title': 'Admin Page',
               'content_title': content_title,
               'add_music_form': AddMusicForm()}

    return render_template('admin.html', context=context)


@app.route('/admin/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_music():
    if request.method == 'POST':
        music_id = request.form['id']
        music_title = request.form['title']
        old_music_title = Music.query.filter(Music.id == music_id).first().title

        secure_edit_music = SecureMusicCRUD(**{'music_title': music_title,
                                               'url_root': request.url_root})
        if secure_edit_music.rename_music_file_in_dir(old_music_title) and secure_edit_music.edit_music_in_db(music_id):
            return redirect(url_for('admin_music_list'))

    content_title = 'Edit music'

    context = {'page_title': 'Admin Page',
               'content_title': content_title,
               'edit_music_form': EditMusicForm()}

    return render_template('admin.html', context=context)


@app.route('/admin/delete', methods=['GET', 'POST'])
@login_required
def admin_delete_music():
    if request.method == 'POST':
        music_id = request.form['id']
        music_title = Music.query.filter(Music.id == music_id).first().title

        secure_delete_music = SecureMusicCRUD(**{'music_title': music_title})
        if secure_delete_music.delete_music_file_from_dir() and secure_delete_music.delete_music_from_db(music_id):
            return redirect(url_for('admin_music_list'))

    content_title = 'Delete music'

    context = {'page_title': 'Admin Page',
               'content_title': content_title,
               'delete_music_form': DeleteMusicForm()}

    return render_template('admin.html', context=context)
