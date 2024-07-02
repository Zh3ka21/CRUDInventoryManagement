from datetime import datetime
from flask import flash
from app.inventory_track import low_stock, record_in_out
from app import db

import logging

def delete_category(category_name: str):
    exist = db.categories.find_one({"name": category_name})
    if not exist:
        logging.error(f"Category '{category_name}' does not exist.")
        return False
    
    db.categories.delete_one({"name": category_name})
    logging.error(f"Category '{category_name}' deleted successfully.")

def add_product(item_name: str, count: int, description: str, category: str, price: int, supplier: str):
    exist = db.items.find_one({"name": item_name})
    if exist:
        flash(f"Item '{item_name}' already exists in the database.", 'error')
        logging.error(f"Item '{item_name}' already exists in the database.")
        return False
    
    item = {
        'name': item_name,
        'count': count,
        'description': description,
        'category': category,
        'created_at': datetime.now(),
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
        
    
    db.items.insert_one(item)
    low_stock(item_name)  
    logging.info(f"Item '{item_name}' added successfully.")
    return True

def update_product(item_name: str, count: int, description: str, category: str, price: int, supplier: str):
    exist = db.items.find_one({"name": item_name})
   
    if exist:
        item = {
            'name': item_name,
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
    else:
        flash(f"Item with name '{item_name}' does not exist.", 'error')
        logging.error(f"Item with name '{item_name}' does not exist.")
        return False

def delete_product(item_name: str):
    exist = db.items.find_one({"name": item_name}, {"_id": 1})
    if not exist:
        logging.error(f"Item '{item_name}' does not exist in the database.")
        flash(f"Item '{item_name}' does not exist in the database.", 'error')
        return False
    
    record_in_out(item_name, "deducted")
    db.items.delete_one({'_id': exist['_id']})
    logging.error(f"Item '{item_name}' deleted successfully.")

def print_info(item_name: str):
    exist = db.items.find_one({"name": item_name})
    if exist:
        created_at = exist.get('created_at', 'N/A')
        updated_at = exist.get('updated_at', 'N/A')
        logging.info(f"Item details:\n"
              f"Name: {exist['name']}\n"
              f"Count: {exist['count']}\n"
              f"Description: {exist['description']}\n"
              f"Category: {exist['category']}\n"
              f"Created At: {created_at}\n"
              f"Updated At: {updated_at}")
    else:
        logging.error(f"Item with name '{item_name}' does not exist.")
        return False

def get_all_products_by_category(category_name: str):
    # Use count_documents to get the product count efficiently
    product_count = db.items.count_documents({"category": category_name})

    if product_count == 0:
        logging.error(f"No products found in category '{category_name}'.")
        return False

    logging.info(f"Products in category '{category_name}':")
    # Iterate through the cursor returned by find
    category = db.items.find({"category": category_name}, {'name': 1, 'count': 1, 'description': 1})
    for product in category:
        logging.info(f"Name: {product['name']}, Count: {product['count']}, Description: {product['description']}")
    return category
