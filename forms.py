from wtforms import Form, StringField, FileField
from wtforms.validators import input_required, regexp


class AddMusicForm(Form):
    title = StringField('Title', validators=[input_required()],
                        render_kw={'placeholder': 'Title'})
    music = FileField('Choose music', id='upload_button',
                      validators=[input_required(), regexp(r'^.+\.mp3$')],
                      render_kw={'accept': '.mp3'})
