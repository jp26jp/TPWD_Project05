from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired()
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
