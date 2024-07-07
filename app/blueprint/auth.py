from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify
from app.login import login, signup
from app._forms.auth_form import RegistrationForm, LoginForm
from flask_login import current_user, login_required, logout_user
from app import db, bcrypt
from bson import ObjectId

from app.forms import AccountForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['POST'])
def register_view():
    if current_user.is_authenticated:
        return jsonify({"message": "Already authenticated"}), 200
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    is_signed = signup(username=username, email=email, password=password)

    if is_signed:
        return jsonify({"message": "Registered successfully"}), 201
    else:
        return jsonify({"error": "Registration failed"}), 400

@auth_bp.route("/login", methods=['POST'])
def login_view():
    if current_user.is_authenticated:
        return jsonify({"message": "Already authenticated"}), 200
        
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    is_logged = login(email=email, password=password)

    if is_logged:
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"error": "Login failed"}), 401

@auth_bp.route("/logout", methods=['POST'])
@login_required
def logout_view():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route("/account", methods=['GET', 'PUT'])
@login_required
def account_view():
    user = db.users.find_one({"_id": ObjectId(current_user.id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        user_data = {
            "username": user.get('username'),
            "email": user.get('email')
        }
        return jsonify(user_data), 200

    if request.method == 'PUT':
        data = request.get_json()
        new_username = data.get('username')
        new_email = data.get('email')
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not current_password:
            return jsonify({"error": "Current password required"}), 400

        if not bcrypt.check_password_hash(user['password'], current_password):
            return jsonify({"error": "Incorrect current password"}), 401

        if new_email and db.users.find_one({'email': new_email}) and new_email != user['email']:
            return jsonify({"error": "Email is already in use by another account"}), 400

        user['username'] = new_username if new_username else user['username']
        user['email'] = new_email if new_email else user['email']

        if new_password:
            if new_password != confirm_password:
                return jsonify({"error": "New passwords do not match"}), 400
            user['password'] = bcrypt.generate_password_hash(new_password).decode('utf-8')

        db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": user})
        return jsonify({"message": "Account information updated successfully"}), 200
    
    