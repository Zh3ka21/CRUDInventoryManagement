from app import db
from datetime import datetime
from bson.objectid import ObjectId
import logging
from flask import flash


def create_order(item_name: str, quantity: int, email: str):
    # Check if the item exists and if there's enough quantity in stock
    item = db.items.find_one({'name': item_name})
    
    if not item:
        logging.error(f"Item '{item_name}' not found in inventory.")
        flash(f"Item '{item_name}' not found in inventory.", 'error')
        return False
    
    if item['count'] < quantity:
        logging.error(f"Not enough '{item_name}' in stock to fulfill order.")
        flash(f"Not enough '{item_name}' in stock to fulfill order.")
        return False
    
    user = db.users.find_one({'email': email}, {'username': 1, 'email': 1})
    if not user:
        logging.error(f"Email '{email}' not found in database. User not registred")
        flash('Failed to find user with such email', 'danger')
        return False
    
    db.items.update_one({'name': item_name}, {'$inc': {'count': -quantity}})
    
    # Log the order in order history
    order = {
        'item_name': item_name,
        'quantity': quantity,
        'email': email,
        'order_date': datetime.now(),
        'status': 'pending' 
    }
    db.orders.insert_one(order)
    
    flash('Order created successfully', 'success')
    logging.info(f"Order created for '{item_name}' (Quantity: {quantity}) by {user['username']}.")
    logging.info(f"Order ID: {order['_id']}")
    return True

# Function to fetch order history
def fetch_order_history():
    orders = db.orders.find({'status': {'$ne': 'completed'}})
    for order in orders:
        logging.info(order)
    return orders

# Function to update order status
def update_order_status(order_id: str, new_status: str):
    try:
        # Convert order_id to ObjectId
        obj_id = ObjectId(order_id)
        result = db.orders.update_one({'_id': obj_id}, {'$set': {'status': new_status}})
        
        if result.matched_count == 0:
            logging.error(f"No order found with ID: {order_id}")
            return False
        else:
            logging.info(f"Order {order_id} status updated to '{new_status}'.")
            return result
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False