from app import db
from datetime import datetime
import logging
from flask import flash, jsonify
from app.products import deduct_quantity
from bson import ObjectId

def convert_ids_to_str(orders):
    return [{**order, '_id': str(order['_id'])} for order in orders]

def create_order(item_name: str, quantity: int, email: str):
    # Check if the item exists and if there's enough quantity in stock
    item = db.items.find_one({'item_name': item_name})
    
    if not item:
        logging.error(f"Item '{item_name}' not found in inventory.")
        flash(f"Item '{item_name}' not found in inventory.", 'error')
        return jsonify({'error': f"Item '{item_name}' not found in inventory."}), 400
    
    if item['count'] < quantity:
        logging.error(f"Not enough '{item_name}' in stock to fulfill order.")
        flash(f"Not enough '{item_name}' in stock to fulfill order.")
        return jsonify({'error': f"Not enough '{item_name}' in stock to fulfill order."}), 400
    
    user = db.users.find_one({'email': email}, {'username': 1, 'email': 1})
    if not user:
        logging.error(f"Email '{email}' not found in database. User not registred")
        flash('Failed to find user with such email', 'danger')
        return jsonify({'error': f"Email '{email}' not found in database. User not registred."}), 400
        
    order = {
        'item_name': item_name,
        'quantity': quantity,
        'email': email,
        'order_date': datetime.now(),
        'status': 'pending' 
    }
    db.orders.insert_one(order)
    
    flash('Order created successfully', 'success')
    return jsonify({"message": "Order created successfully"}, 200)  

def fetch_order_history(email):
    if email:
        orders = db.orders.find({'email': email})
    else:
        orders = db.orders.find()
    orders_list = list(orders)
    return {"orders": convert_ids_to_str(orders_list)}

def update_order_status(id: str, new_status: str):
    try:
        _id = ObjectId(id)
        # Attempt to update the order status
        result = db.orders.update_one({'_id': _id}, {'$set': {'status': new_status}})
        
        # Check if the update was successful
        if result.modified_count > 0:
            if new_status == 'completed':
                quantity_cursor = db.orders.find_one({'_id': _id}, {'quantity': 1, 'item_name': 1})

                if quantity_cursor:
                    deduct_quantity(quantity_cursor['item_name'], quantity_cursor['quantity'])
                else:
                    flash(f"Failed to find quantity for order '{id}'.", 'error')

            return jsonify({'message': "Updated correctly"}), 200
        else:
            flash(f"Failed to update order '{id}' status. Order not found or status unchanged.", 'error')
            return jsonify({'error': f"Failed to update order '{id}' status. Order not found or status unchanged."}), 400

    except Exception as e:
        flash(f"An error occurred while updating order '{id}': {e}", 'error')
        logging.error(f"An error occurred while updating order '{id}': {e}")
        return jsonify({'error': f"An error occurred while updating order '{id}': {e}"}), 400