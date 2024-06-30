from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.login import login, signup
from app.forms.auth_form import RegistrationForm, LoginForm
from flask_login import current_user, login_required, logout_user
from app import db, bcrypt
from bson import ObjectId


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password = form.password.data

        # Process signup logic
        is_signed = signup(username=username, email=email, password=password)

        if is_signed:
            return redirect(url_for('auth.login_view'))
        else:
            flash("Registration failed. Please try again.", "error")

    return render_template('register.html', title='Register', form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Process login logic
        is_logged = login(email=email, password=password)

        if is_logged:
            return redirect(url_for('home'))
        else:
            flash("Login failed. Please check your credentials.", "error")

    return render_template('login.html', title='Login', form=form)

@auth_bp.route("/logout")
def logout_view():
    logout_user()
    return redirect(url_for('home'))

@auth_bp.route("/account", methods=['POST', 'GET'])
@login_required
def account_view():
    user = db.users.find_one({"_id": ObjectId(current_user.id)})

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validate new email
        if db.users.find({'email': new_email}):
            flash('Incorrect new email.', 'error')
            return redirect(url_for('auth.account_view'))

        # Validate current password
        if not bcrypt.check_password_hash(user['password'], current_password):
            flash('Incorrect current password.', 'error')
        else:
            # Update user data
            user['username'] = new_username
            user['email'] = new_email

            # Update password if new_password is provided and matches confirm_password
            if new_password and new_password == confirm_password:
                user['password'] = bcrypt.generate_password_hash(new_password).decode('utf-8')


            # Save user data back to the database
            db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": user})
            flash('Account information updated successfully.', 'success')

            # Redirect to prevent form resubmission on refresh
            return redirect(url_for('home'))
    
    return render_template('account.html', title='Account', user=user)