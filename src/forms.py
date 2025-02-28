from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, DateField, TextAreaField
from wtforms.validators import DataRequired

class editBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], )

