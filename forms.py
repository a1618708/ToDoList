from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ToDoForm(FlaskForm):
    name = StringField(label="Name")
    text = StringField(label="")
    add = SubmitField(label="Add")