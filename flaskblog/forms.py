from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields import SelectField
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        if not email.data.endswith('@rvce.edu.in'):
            raise ValidationError('Email must be from the "@rvce.edu.in" domain.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            if not email.data.endswith('@rvce.edu.in'):
                raise ValidationError('Email must be from the "@rvce.edu.in" domain.')
            
class PostForm(FlaskForm):
    title = StringField('Product Name', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    price = IntegerField('Price (Rs)', validators=[DataRequired()])
    category = SelectField('Choose Category', choices=[('project_items', 'Project Items'),
                                                       ('books', 'Books'),
                                                       ('miscellaneous', 'Miscellaneous')],
                           validators=[DataRequired()])
    submit = SubmitField('Post')

    # def validate_price(self, price):
    #     if price.data is None or price.data == '':
    #         raise ValidationError('Price is required')
    #     if int(price.data) < 0:
    #         raise ValidationError('Price cannot be negative')