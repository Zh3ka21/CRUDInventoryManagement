from app import db
from datetime import datetime
import logging

from flask import flash

THRESHOLD = 5

# Function to check for low stock and return the item name if stock is low
def low_stock(name: str):
    item = db.items.find_one({'name': name}, {'name': 1, 'count': 1})
    if item and item['count'] < THRESHOLD:
        logging.info(f"Item {item['name']} is on low stock, its count {item['count']} < {THRESHOLD}")
        flash(f"Item {item['name']} is on low stock, its count {item['count']} < {THRESHOLD}", "warning")

# Function to record stocks
def record_in_out(item_name: str, action: str):
    quantity = db.items.find_one({'name': item_name})
    
    with open('log.txt', 'a') as f:
        f.write(f'{item_name} was {action} in {quantity} on {datetime.now()} \n')

# Function to fetch items with stock levels below the threshold
def fetch_stocks():
    items = db.items.find({"count": {"$lt": THRESHOLD}})
    docs = list(items)
    for doc in docs:
        logging.info(doc)
        
    return docs