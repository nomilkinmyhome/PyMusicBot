from PyMusicBot.views import Auth, Logout, MusicList, AddMusic, EditMusic, DeleteMusic


def init_routes(app):
    app.add_url_rule('/', view_func=Auth.as_view('auth'))
    app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
    app.add_url_rule('/admin/list', view_func=MusicList.as_view('admin_music_list'))
    app.add_url_rule('/admin/add', view_func=AddMusic.as_view('admin_add_music'))
    app.add_url_rule('/admin/edit', view_func=EditMusic.as_view('admin_edit_music'))
    app.add_url_rule('/admin/delete', view_func=DeleteMusic.as_view('admin_delete_music'))
