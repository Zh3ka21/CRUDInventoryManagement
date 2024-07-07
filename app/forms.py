from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
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
    
