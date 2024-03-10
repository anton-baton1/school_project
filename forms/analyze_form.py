from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AnalyzeForm(FlaskForm):
    input_word = StringField("")
    submit = SubmitField("Разобрать")
