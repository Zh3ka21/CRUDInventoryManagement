from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

class AccountForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired()])
    email = StringField('New Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update')

class OrderForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])

class StatusForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')        
    ], validators=[DataRequired()])
    
class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class ProductForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    price_per_unit = FloatField('Price per Unit', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    