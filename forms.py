from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import (DataRequired, ValidationError)

from models import Entry


def title_exists(field):
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
    time_spent = IntegerField(
        'Time Spent',
        validators=[DataRequired()]
    )
    learned = TextAreaField(
        'What I Learned',
        validators=[DataRequired()]
    )
    resources = TextAreaField(
        'Resources to Remember',
        validators=[DataRequired()]
    )
