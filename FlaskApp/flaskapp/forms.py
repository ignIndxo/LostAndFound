from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from flaskapp.models import Users, Rentals

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=16)]) 
    # Usernames can only be between 6 and 16 characters and something has to be entered
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Passwords can only be 6 or more characters
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken, please choose another one')

class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    typeOfClothing = SelectField('Type of Clothing', choices=[('Dress'), ('Suit'), ('Costume'), ('Shirt'), ('Tshirt'), ('Trousers'), ('Shorts'), ('Skirt')], validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    brand = StringField('Brand')
    colour = SelectField('Colour', choices=[('White'), ('Black'), ('Grey'), ('Brown'), ('Beige'), ('Pink'), ('Red'), ('Orange'), ('Yellow'), ('Green'), ('Blue'), ('Purple')], validators=[DataRequired()])
    size = SelectField('Size', choices=[('XXS'), ('XS'), ('S'), ('M'), ('L'), ('XL'), ('XXL')], validators=[DataRequired()])
    minimumCredits = IntegerField('Minimum Credits', validators=[DataRequired()])
    submit = SubmitField('Upload')

class ItemRental(FlaskForm):
    startDate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    endDate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Rent')