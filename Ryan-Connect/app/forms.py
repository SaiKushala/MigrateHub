from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, Optional
from app.models import User
import pycountry

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    preferred_language = SelectField('Preferred Language',
                                     choices=[(lang.alpha_2, lang.name) for lang in pycountry.languages if hasattr(lang, 'alpha_2')],
                                     validators=[DataRequired()])
    country = SelectField('Country',
                          choices=[(country.alpha_2, country.name) for country in pycountry.countries],
                          validators=[DataRequired()], id='country')
    state = SelectField('State',
                        choices=[], id='state')
    city = SelectField('City',
                       choices=[], id='city')
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message='Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.')
    ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class SearchForm(FlaskForm):
    from_country = SelectField('From Country', choices=[], validators=[DataRequired(message="Please select a 'From Country'.")])
    from_state = SelectField('From State', choices=[], validators=[Optional()])
    from_city = SelectField('From City', choices=[], validators=[Optional()])
    to_country = SelectField('To Country', choices=[], validators=[DataRequired(message="Please select a 'To Country'.")])
    to_state = SelectField('To State', choices=[], validators=[Optional()])
    to_city = SelectField('To City', choices=[], validators=[Optional()])
    submit = SubmitField('Search')
