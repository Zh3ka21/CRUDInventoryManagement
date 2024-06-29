from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.login import login, signup

from app.forms.auth_form import RegistrationForm, LoginForm

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
        else:
            flash("Something wrong occured", "error")
    
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


