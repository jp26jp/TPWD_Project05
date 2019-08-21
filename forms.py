from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import (DataRequired, ValidationError)

from models import Entry


def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError('An entry with that title already exists.')


class RegisterForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            title_exists
        ]
    )
    date = DateField(
        'Date',
        validators=[DataRequired()]
    )
    time_spent = DateField(
        'Time spent',
        validators=[DataRequired()]
    )
    learned = DateField(
        'Learned',
        validators=[DataRequired()]
    )
    resources = DateField(
        'Resources',
        validators=[DataRequired()]
    )
