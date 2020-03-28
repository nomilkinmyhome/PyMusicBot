from models import Music, User
from forms import AddMusicForm, EditMusicForm, DeleteMusicForm, AuthForm
from utils import SecureMusicCRUD

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask.views import View, MethodView
from werkzeug.exceptions import BadRequestKeyError


class BasePage(MethodView):
    decorators = [login_required]
    context_objects = {}

    def get(self):
        self.context_objects['page_title'] = 'Admin Page'
        return self.render_template(self.context_objects)

    def post(self):
        pass

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get_template_name(self):
        return 'admin.html'


class Auth(BasePage):
    decorators = []
    context_objects = {'page_title': 'Log in',
                       'auth_form': AuthForm()}

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin_music_list'))

        return self.render_template(self.context_objects)

    def post(self):
        user = User.query.filter_by(name=request.form['login']).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user, remember=True)

            return redirect(url_for('admin_music_list'))

    def get_template_name(self):
        return 'auth.html'


class Logout(View):
    decorators = [login_required]

    def dispatch_request(self):
        logout_user()

        return redirect(url_for('auth'))


class MusicList(View):
    decorators = [login_required]

    def dispatch_request(self):
        content_title = 'Music list'

        context = {'page_title': 'Admin Page',
                   'content_title': content_title,
                   'search': self.get_search(),
                   'pages': self.get_pages()}

        return self.render_template(context)

    def get_search(self):
        return request.args.get('search')

    def get_pages(self):
        current_page = self.get_current_page()
        music_list = self.get_music_list()

        return music_list.paginate(page=current_page, per_page=10)

    def get_current_page(self):
        current_page = request.args.get('page')

        if current_page and current_page.isdigit():
            current_page = int(current_page)
        else:
            current_page = 1

        return current_page

    def get_music_list(self):
        search = self.get_search()
        if search:
            return Music.query.filter(Music.title.ilike(f'%{search}%'))
        else:
            return Music.query.order_by(Music.pub_date.desc())

    def render_template(self, context):
        return render_template('admin.html', **context)


class AddMusic(BasePage):
    context_objects = {'content_title': 'Add music',
                       'add_music_form': AddMusicForm()}

    def post(self):
        try:
            music_title = request.form['title']
            music_file = request.files['music']

            secure_save = SecureMusicCRUD(**{'music_title': music_title,
                                             'url_root': request.url_root})
            if secure_save.save_to_dir(music_file) and secure_save.save_to_db():
                return redirect(url_for('admin_music_list'))
        except BadRequestKeyError:
            pass


class EditMusic(BasePage):
    context_objects = {'content_title': 'Edit music',
                       'edit_music_form': EditMusicForm()}

    def post(self):
        music_id = request.form['id']
        music_title = request.form['title']
        old_music_title = Music.query.filter(Music.id == music_id).first().title

        secure_edit_music = SecureMusicCRUD(**{'music_title': music_title,
                                               'url_root': request.url_root})
        if secure_edit_music.rename_music_file_in_dir(old_music_title) and secure_edit_music.edit_music_in_db(music_id):
            return redirect(url_for('admin_music_list'))


class DeleteMusic(BasePage):
    context_objects = {'content_title': 'Delete music',
                       'delete_music_form': DeleteMusicForm()}

    def post(self):
        music_id = request.form['id']
        music_title = Music.query.filter(Music.id == music_id).first().title

        secure_delete_music = SecureMusicCRUD(**{'music_title': music_title})
        if secure_delete_music.delete_music_file_from_dir() and secure_delete_music.delete_music_from_db(music_id):
            return redirect(url_for('admin_music_list'))
