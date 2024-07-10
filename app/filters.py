from app import db
from app.inventory_track import low_stock

from flask import flash, jsonify

def search_products(name=None, category=None, isLow: bool = True):
    query = {}
    
    if name:
        query['item_name'] = {'$regex': name, '$options': 'i'}  # Case-insensitive search
    if category:
        query['category'] = category
    
    products_cursor = db.items.find(query, {'_id': 0})  

    products = []
    for product in products_cursor:
        if isLow:
            low_stock(product['item_name'])
        products.append(product)
        
    if len(products) == 0:
        flash("No such product found", "error")
        return jsonify({"No such product found"}, 400)
    return list(products)

def filter_products(criteria):
    query = {}
    
    for key, value in criteria.items():
        if key == 'item_name':
            query['item_name'] = {'$regex': value, '$options': 'i'}  # Case-insensitive search
        elif key == 'category':
            query['category'] = value
        elif key == 'price':
            query['price_per_unit'] = value 
    
    products = db.items.find(query, {'_id': 0})
    return list(products)