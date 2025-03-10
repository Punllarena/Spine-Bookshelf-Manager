from flask_wtf import FlaskForm
from wtforms import  SubmitField, FileField
from wtforms.validators import DataRequired, InputRequired

# class editBookForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()], )

class UploadBackupForm(FlaskForm):
    file = FileField('Upload CSV', validators=[InputRequired()])
    submit = SubmitField('Upload')