from PyMusicBot import logger
from PyMusicBot.forms import AddMusicForm, EditMusicForm, DeleteMusicForm, AuthForm
from PyMusicBot.controllers import authorization, pagination, crud_manager

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from flask.views import View, MethodView

from werkzeug.datastructures import FileStorage
from typing import Union, Dict


class BasePage(MethodView):
    decorators: list = [login_required]
    template: str = ''

    def get(self) -> Union[redirect, render_template]:
        context: dict = self.get_context()
        if 'page_title' not in context:
            context['page_title'] = 'Admin Page'

        return self.render_template(context)

    def post(self) -> Union[None, redirect]:
        pass

    def render_template(self, context) -> render_template:
        return render_template(self.template, **context)

    def get_context(self) -> dict:
        raise NotImplementedError


class Auth(BasePage):
    decorators: list = []
    template: str = 'auth.html'

    def get(self) -> Union[redirect, render_template]:
        if current_user.is_authenticated:
            return redirect(url_for('admin_music_list'))

        return self.render_template(self.get_context())

    def post(self) -> redirect:
        form = AuthForm(request.form)
        if form.validate():
            if authorization.by_login(login=request.form['login'],
                                      password=request.form['password']):

                return redirect(url_for('admin_music_list'))
            else:
                flash('Incorrect login or password!')

        return redirect(url_for('auth'))

    def get_context(self) -> Dict[str, Union[str, AuthForm]]:
        context: Dict[str, Union[str, AuthForm]] = {'page_title': 'Log in',
                                                    'auth_form': AuthForm()}

        return context


class Logout(View):
    decorators: list = [login_required]

    def dispatch_request(self) -> redirect:
        logout_user()

        return redirect(url_for('auth'))


class MusicList(BasePage):
    decorators: list = [login_required]
    template: str = 'music_list.html'

    def get_context(self) -> Dict[str, Union[str, None]]:
        search: Union[str, None] = request.args.get('search')
        current_page: int = int(request.args.get('page')) if str(request.args.get('page')).isdigit() else 1

        context: Dict[str, Union[str, None]] = {'content_title': 'Music list',
                                                'search': search,
                                                'pages': pagination.get_pages(current_page, search)}

        return context


class AddMusic(BasePage):
    decorators: list = [login_required]
    template: str = 'add_music.html'

    def post(self) -> redirect:
        form = AddMusicForm(request.files)
        if form.music.data:
            if form.music.data.filename.endswith('.mp3') and form.music.data.mimetype == 'audio/mpeg':
                music_title: str = request.form.get('title', '')
                music_file: FileStorage = request.files.get('music', None)

                if crud_manager.save(music_title, music_file):
                    return redirect(url_for('admin_music_list'))
                else:
                    logger.warning('Unsuccessful attempt to add music')
                    flash('Something went wrong...')
            else:
                flash('The music file must be .mp3!')

        return redirect(url_for('admin_add_music'))

    def get_context(self) -> Dict[str, Union[str, AddMusicForm]]:
        context: Dict[str, Union[str, AddMusicForm]] = {'content_title': 'Add music',
                                                        'add_music_form': AddMusicForm()}

        return context


class EditMusic(BasePage):
    template: str = 'edit_music.html'

    def post(self) -> Union[redirect, None]:
        form = EditMusicForm(request.form)
        if form.validate():
            try:
                music_title: str = request.form['title']
                music_id: str = request.form['id']
            except AttributeError:
                flash('No music with that ID')
                return redirect(url_for('admin_edit_music'))

            if crud_manager.edit(music_title, music_id):
                return redirect(url_for('admin_music_list'))
            else:
                logger.warning('Unsuccessful attempt to edit music')
                flash('Server error!')
        else:
            flash('Incorrect data!')

        return redirect(url_for('admin_edit_music'))

    def get_context(self) -> Dict[str, Union[str, EditMusicForm]]:
        context: Dict[str, Union[str, EditMusicForm]] = {'content_title': 'Edit music',
                                                         'edit_music_form': EditMusicForm()}

        return context


class DeleteMusic(BasePage):
    template: str = 'delete_music.html'

    def post(self) -> redirect:
        form = DeleteMusicForm(request.form)
        if form.validate():
            try:
                music_id: str = request.form['id']
            except AttributeError:
                flash('No music with that ID')
                return redirect(url_for('admin_delete_music'))

            if crud_manager.delete(music_id):
                return redirect(url_for('admin_music_list'))
            else:
                logger.warning('Unsuccessful attempt to delete music')
                flash('Server error!')
        else:
            flash('Incorrect ID!')

        return redirect(url_for('admin_delete_music'))

    def get_context(self) -> Dict[str, Union[str, DeleteMusicForm]]:
        context: Dict[str, Union[str, DeleteMusicForm]] = {'content_title': 'Delete music',
                                                           'delete_music_form': DeleteMusicForm()}

        return context
