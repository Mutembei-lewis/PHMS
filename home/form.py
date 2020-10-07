from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, DateField,IntegerField,SelectField, TextField,SubmitField,FileField,TextAreaField,PasswordField
from wtforms.validators import ValidationError, DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from home.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email(message="Not a valid email address ")])
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password',message='The passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email:',validators=[DataRequired(message='This must be filled'),Email(message= "This field must be an email")])
    password = PasswordField('password:',validators = [DataRequired(message="This field is required")])
    submit= SubmitField('Log in')

class RequestResetForm(FlaskForm):
        email = StringField("Email",
                            validators=[DataRequired(),Email()])
        submit = SubmitField('Request password reset ')
        def validate_email(self, email):
            user = User.query.filter_by(email = email.data).first()
            if user is None:
                raise ValidationError('There is no account with that email . You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators =[DataRequired(),])
    confirm_password = PasswordField("confirm password", validators =[DataRequired(),EqualTo('password')])
    submit = SubmitField("Reset Password")

class UpdateProfile(FlaskForm):
        avatar = FileField('image',validators=[FileAllowed(['gif', 'jpg', 'jpeg', 'png'],'Images only can be uploaded')] )
        submit = SubmitField('Submit')



# if a form doesnt use flask form you can use 
# value="{{ csrf_token() }}" property in the input tag
 