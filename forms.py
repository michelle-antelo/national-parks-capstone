from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, validators, ValidationError
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    bio = TextAreaField('Share a little about yourself', validators=[Length(max=60)])