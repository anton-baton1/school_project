from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField("Job Title", validators=[DataRequired()])
    team_leader = IntegerField("Team leader id", validators=[DataRequired()])
    work_size = IntegerField("Work Size", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Submit')
