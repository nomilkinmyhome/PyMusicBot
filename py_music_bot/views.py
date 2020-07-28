"""This module contains views of all pages of the site"""

from typing import Union, Dict
import logging.config
from .config import logger_config

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from flask.views import View, MethodView
from werkzeug.datastructures import FileStorage

from py_music_bot.forms import AddMusicForm, EditMusicForm, DeleteMusicForm, AuthForm
from py_music_bot.use_cases import authorization, pagination, crud_manager

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')


class BasePage(MethodView):
    """Base class for all page classes.

    :var: decorators - list of the decorators
    :var: template - html-template for rendering
    """

    decorators: list = [login_required]
    template: str = ''

    def get(self):
        """Get request handler"""

        context: dict = self.get_context()
        return self.render_template(context)

    def post(self):
        """Post request handler"""

        pass

    def render_template(self, context) -> render_template:
        """Render method"""

        return render_template(self.template, **context)

    def get_context(self) -> dict:
        """Must be overriden.

        :returns: context - dictionary with all required fields for rendering.
        """

        raise NotImplementedError


class Auth(BasePage):
    decorators: list = []
    template: str = 'auth.html'

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin_music_list'))

        return self.render_template(self.get_context())

    def post(self):
        form = AuthForm(request.form)
        if form.validate():
            try:
                authorization.by_login(login=request.form['login'],
                                       password=request.form['password'])

                return redirect(url_for('admin_music_list'))
            except ValueError:
                flash('Incorrect login or password!')

        return redirect(url_for('auth'))

    def get_context(self) -> Dict[str, Union[str, AuthForm]]:
        context: Dict[str, Union[str, AuthForm]] = {'auth_form': AuthForm()}

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
        if form.music.data and form.music.data.filename.endswith('.mp3'):
            try:
                music_title: str = request.form['title']
                music_file: FileStorage = request.files['music']

                crud_manager.save(music_title, music_file)
                return redirect(url_for('admin_music_list'))
            except KeyError:
                flash('All fields are required!')
            except ValueError:
                logger.error('Unsuccessful attempt to add music: the title is too long!')
                flash('The title is too long!')
        else:
            flash('The music file must be .mp3!')

        return redirect(url_for('admin_add_music'))

    def get_context(self) -> Dict[str, Union[str, AddMusicForm]]:
        context: Dict[str, Union[str, AddMusicForm]] = {'content_title': 'Add music',
                                                        'add_music_form': AddMusicForm()}

        return context


class EditMusic(BasePage):
    template: str = 'edit_music.html'

    def post(self):
        form = EditMusicForm(request.form)
        if form.validate():
            try:
                music_title: str = request.form['title']
                music_id: str = request.form['id']

                crud_manager.edit(music_title, music_id)
                return redirect(url_for('admin_music_list'))
            except FileNotFoundError:
                logger.error('Unsuccessful attempt to edit music: file not found!')
                flash('File not found!')
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

                crud_manager.delete(music_id)
                return redirect(url_for('admin_music_list'))
            except FileNotFoundError:
                logger.error('Unsuccessful attempt to delete music: file not found!')
                flash('File not found!')
        else:
            flash('Incorrect ID!')

        return redirect(url_for('admin_delete_music'))

    def get_context(self) -> Dict[str, Union[str, DeleteMusicForm]]:
        context: Dict[str, Union[str, DeleteMusicForm]] = {'content_title': 'Delete music',
                                                           'delete_music_form': DeleteMusicForm()}

        return context
