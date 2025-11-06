from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Form(FlaskForm):
	repoPath = StringField('repo', validators=[DataRequired()])
	submit = SubmitField('Analyze')