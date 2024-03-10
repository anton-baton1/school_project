from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AnalyzeForm(FlaskForm):
    input_word = StringField("")
    submit = SubmitField("Разобрать")
