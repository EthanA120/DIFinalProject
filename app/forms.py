from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task = StringField('NewTask', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    submit = SubmitField('AddButton')


class ClearForm(FlaskForm):
    clear = SubmitField('Clear')
