import logging
from flask import flash, redirect, request, url_for
from flask_login import login_user, UserMixin
from app import db, bcrypt
from bson import ObjectId
from app import login_manager


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.status = user_data['role']

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

def login(email: str, password: str):
    user_data = db.users.find_one({"email": email})

    if user_data is None:
        logging.error(f"User with email {email} not found.")
        flash("User wasn't found!", "error")
        return False

    if bcrypt.check_password_hash(user_data['password'], password):
        logging.info(f"{user_data['email']} logged in successfully")
        flash("Logged in successfully", "success")
        user = User(user_data)
        login_user(user)
        return True
    else:
        logging.error("Incorrect password")
        flash("Incorrect password!", "error")
        return False

def signup(username: str, email: str, password: str):
    exist_user = db.users.find_one({"email": email})
    if exist_user:
        logging.error(f"User with email {email} already exists.")
        flash("User with this email already exists.", "error")
        return False

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "role": "user"
    }

    db.users.insert_one(new_user)
    logging.info(f"User {email} registered successfully")
    flash("Registered successfully. Please log in.", "success")
    return True
