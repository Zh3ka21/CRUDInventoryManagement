from app import db
from app.inventory_track import low_stock

def search_products(name=None, category=None, isLow: bool = True):
    query = {}
    
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}  # Case-insensitive search
    if category:
        query['category'] = category
    
    products_cursor = db.items.find(query, {'_id': 0})  

    products = []
    for product in products_cursor:
        if isLow:
            low_stock(product['name'])
        products.append(product)
    return list(products)

def filter_products(criteria):
    query = {}
    
    for key, value in criteria.items():
        if key == 'name':
            query['name'] = {'$regex': value, '$options': 'i'}  # Case-insensitive search
        elif key == 'category':
            query['category'] = value
        elif key == 'price':
            query['price_per_unit'] = value 
    
    products = db.items.find(query, {'_id': 0})
    return list(products)