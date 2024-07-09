from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify
from app.login import login, signup
from app._forms.auth_form import RegistrationForm, LoginForm, AccountForm
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

        is_signed = signup(username=username, email=email, password=password)

        if is_signed:
            flash("Registered successfully. Redirecting to login...", "success")
            return redirect(url_for('auth.login_view'))
        else:
            flash("Registration failed", "danger")
            return redirect(url_for('home'))

    return render_template('register.html', form=form)


@auth_bp.route("/login", methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        is_logged = login(email=email, password=password)

        if is_logged:
            flash("Logged in successfully", "success")
            return redirect(url_for('home'))
        else:
            flash("Login failed", "danger")
    return render_template('login.html', form=form)

@auth_bp.route("/logout", methods=['GET'])
@login_required
def logout_view():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('home'))

@auth_bp.route("/account", methods=['GET'])
@login_required
def account_view():
    form = AccountForm()
    return render_template('account.html', form=form)

@auth_bp.route("/account/data", methods=['GET'])
@login_required
def account_data():
    user = db.users.find_one({"_id": ObjectId(current_user.id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"email": user['email'], "username": user['username'], 'role': user['role']})

@auth_bp.route("/account", methods=['PUT'])
@login_required
def account_update():
    form = AccountForm()

    if form.validate_on_submit():
        user = db.users.find_one({"_id": ObjectId(current_user.id)})
        new_username = form.username.data
        new_email = form.email.data
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if new_email != user['email'] and db.users.find_one({'email': new_email}):
            return jsonify({'error': 'Email is already in use by another account.'}), 400

        if not bcrypt.check_password_hash(user['password'], current_password):
            return jsonify({'error': 'Incorrect current password.'}), 400

        user['username'] = new_username
        user['email'] = new_email

        if new_password and new_password == confirm_password:
            user['password'] = bcrypt.generate_password_hash(new_password).decode('utf-8')

        db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": user})
        return jsonify({'message': 'Account updated successfully.'}), 200

    return jsonify({'error': 'Invalid form data.'}), 400