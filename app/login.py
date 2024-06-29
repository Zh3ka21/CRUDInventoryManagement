from set_up import db
import logging


def login(email: str, password:  str):
    user = db.users.find_one({"email": email}, {"email": 1, "password": 1, "_id": 0})
    print(user)
    print(email, password)
    
    if user and user['password'] == password:     
        logging.info( f"{user['email']} logged in successfully")
        return True
    
    elif user['password'] != password:
        logging.error(f"Incorrect user password")
        return False
    
    else:
        logging.error(f"No user was found with email {user['email']}")
        return False

def signup(username: str, email: str, password:  str):
    exist_user = db.users.find_one({'email': email}, {'email': 1, "_id": 0})
    if exist_user:
        logging.error( f"User with such email {exist_user['email']} exists." ) 
        return False
    
    nuser = {"username": username, "email": email, "password": password, "role": "user"}
    db.users.insert_one(nuser)
    return True