from datetime import datetime
from flask import flash, jsonify
from app.inventory_track import low_stock, record_in_out
from app import db
from bson import ObjectId

import logging

def add_product(item_name: str, count: int, description: str, category: str, price: int, supplier: str):
    exist = db.items.find_one({"item_name": item_name})
    
    if exist:
        if exist['count'] < count:
            record_in_out(item_name, "added")
        elif exist['count'] > count:
            record_in_out(item_name, "deducted")
        else:
            record_in_out(item_name, "No changes with count")
          
        flash(f"Item '{item_name}' already exists in the database.", 'error')
        return jsonify({'error': f"Item '{item_name}' already exists in the database."}), 400
    
    item = {
        'item_name': item_name,
        'count': count,
        'description': description,
        'category': category,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'price_per_unit': price,
        'supplier': supplier
    }

    record_in_out(item_name, "added")
    db.items.insert_one(item)
    low_stock(item_name)  
    logging.info(f"Item '{item_name}' added successfully.")
    return jsonify({"message": f"Item '{item_name}' added successfully."}, 201)

def update_product(_id: str, item_name: str, count: int, description: str, category: str, price: int, supplier: str):
    exist = db.items.find_one({"_id": ObjectId(_id)})
   
    if exist:
        item = {
            'item_name': item_name,
            'count': count,
            'description': description,
            'category': category,
            'updated_at': datetime.now(),
            'price_per_unit': price,
            'supplier': supplier
        }

        if exist['count'] < count:
            record_in_out(item_name, "added")
        elif exist['count'] > count:
            record_in_out(item_name, "deducted")
        else:
            record_in_out(item_name, "No changes with count")  
                  
        db.items.update_one({'_id': exist['_id']}, {'$set': item})
        low_stock(item_name)   
        logging.info(f"Item '{item_name}' updated successfully.")
        return jsonify({"message": f"Item '{item_name}' updated successfully."}, 200)
    else:
        flash(f"Item with name '{item_name}' does not exist.", 'error')
        logging.error(f"Item with name '{item_name}' does not exist.")
        return jsonify({"error": f"Item with name '{item_name}' does not exist."}, 400)

def delete_product(id: str):
    exist = db.items.find_one({"_id": id}, {"_id": 1, 'item_name': 1})
    if not exist:
        jsonify({f"Item '{exist['item_name']}' does not exist in the database."}, 400)
        flash(f"Item '{exist['item_name']}' does not exist in the database.", 'error')
        return False
    
    record_in_out(exist['item_name'], "deducted")
    db.items.delete_one({'_id': exist['_id']})
    return jsonify({"message": f"Item '{id}' deleted successfully."}, 200)

def get_all_products():
    return list(db.items.find({}))

def deduct_quantity(name: str, quantity: int):
    db.items.update_one({'item_name': name}, {'$inc': {'count': -quantity}})
    low_stock(name)
    record_in_out(name, "deducted")
    return jsonify({"message": f"Item '{name}' deducted by '{quantity}' successfully."}, 200)  