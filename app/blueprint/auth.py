import email
from math import log
from flask import Blueprint, render_template, request, redirect, url_for, flash
from login import login, signup

from models.auth_form import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=['GET', 'POST'])
def register_view():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password = form.password.data
        
        # Process signup logic (e.g., storing user in database)
        isSigned = signup(username=username, email=email, password=password)

        if isSigned:
            return redirect(url_for('home'))
    
    return render_template('register.html', title='Register', form=form)



@auth_bp.route("/login", methods=['GET', 'POST'])
def login_view():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Process login logic (e.g., verifying credentials)
        isLogged = login(email=email, password=password)

        if isLogged:
            return redirect(url_for('home'))
    
    return render_template('login.html', title='Login', form=form)




















# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login_view():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         if login(email, password):
#             flash('Logged in successfully!', 'success')
#             return redirect(url_for('dashboard'))  # Assuming 'dashboard' is the function name in app.py
#         else:
#             flash('Login failed. Check your email and password.', 'danger')
#     return render_template('login.html')

# @auth_bp.route('/signup', methods=['GET', 'POST'])
# def signup_view():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         if signup(username, email, password):
#             flash('Signed up successfully!', 'success')
#             return redirect(url_for('auth.login_view'))  # Redirect to login view after successful signup
#         else:
#             flash('Sign up failed. Email may already be in use.', 'danger')
#     return render_template('signup.html')
