from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired,Email,EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username', validators =[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password1 = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password1')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me',validators= [DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    priority = SelectField(u'Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    labels = SelectMultipleField(u'Labels', choices=[('food', 'Food'), ('cloth', 'Clothing'), ('clean', 'Cleaning'), ('entertain', 'Entertainment'), ('room', 'Room Maintainance')])
    submit = SubmitField('Create Task')