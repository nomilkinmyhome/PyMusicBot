from wtforms import Form, StringField, FileField, IntegerField, PasswordField
from wtforms.validators import input_required, regexp


class AddMusicForm(Form):
    title = StringField('Title', validators=[input_required()],
                        render_kw={'placeholder': 'Title'})
    music = FileField('Choose music', id='upload_button',
                      validators=[input_required(), regexp(r'^.+\.mp3$')],
                      render_kw={'accept': '.mp3'})


class EditMusicForm(Form):
    id = IntegerField('ID', validators=[input_required()],
                      render_kw={'placeholder': 'Music ID'})
    title = StringField('New title', validators=[input_required()],
                        render_kw={'placeholder': 'New title'})


class DeleteMusicForm(Form):
    id = IntegerField('ID', validators=[input_required()],
                      render_kw={'placeholder': 'Music ID'})


class AuthForm(Form):
    login = StringField('Login', validators=[input_required()],
                        render_kw={'placeholder': 'Login'})
    password = PasswordField('Password', validators=[input_required()],
                             render_kw={'placeholder': 'Password'})
