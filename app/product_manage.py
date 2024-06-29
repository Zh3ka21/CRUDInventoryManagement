from datetime import datetime
from set_up import db
from inventory_track import low_stock

import logging

def add_category(category_name: str):
    exist = db.categories.find_one({"name": category_name})
    if exist:
        logging.error(f"Category '{category_name}' already exists.")
        return False
    
    category = {
        'name': category_name,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    db.categories.insert_one(category)
    logging.info(f"Category '{category_name}' added successfully.")

def add_supplier(supplier_name: str):
    exist = db.suppliers.find_one({"name": supplier_name})
    if exist:
        logging.error(f"Supplier '{supplier_name}' already exists.")
        return False
    
    category = {
        'name': supplier_name,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    db.suppliers.insert_one(category)
    logging.info(f"Category '{supplier_name}' added successfully.")

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
    
    low_stock(item_name)  
    
    db.items.insert_one(item)
    logging.info(f"Item '{item_name}' added successfully.")

def update_product(item_name: str, count: int, description: str, category: str, price: int, supplier: str):
    exist_id = db.items.find_one({"name": item_name}, {'_id': 1})
   
    if exist_id:
        item = {
            'name': item_name,
            'count': count,
            'description': description,
            'category': category,
            'updated_at': datetime.now(),
            'price_per_unit': price,
            'supplier': supplier
        }
        
        low_stock(item_name)      
          
        db.items.update_one({'_id': exist_id['_id']}, {'$set': item})
        logging.info(f"Item '{item_name}' updated successfully.")
    else:
        logging.error(f"Item with name '{item_name}' does not exist.")
        return False

def delete_product(item_name: str):
    exist = db.items.find_one({"name": item_name}, {"_id": 1})
    if not exist:
        logging.error(f"Item '{item_name}' does not exist in the database.")
        return False
    
    db.items.delete_one({'_id': exist['_id']})
    logging.error(f"Item '{item_name}' deleted successfully.")

def get_info(item_name: str):
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

#increment
def inc_dec_item(item_name: str, count: int):
    item = db.items.find_one({'name': item_name})
    if not item:
        logging.error(f"Item '{item_name}' not found in inventory.")
        return False
    
    # Update the item's count
    new_count = item['count'] + count
    if new_count < 0:
        logging.error(f"Cannot decrement '{item_name}' below zero. Current count: {item['count']}.")
        return False
    
    db.items.update_one({'name': item_name}, {'$inc': {'count': count}})
    logging.info(f"Item '{item_name}' count updated to {new_count}.")