from set_up import db

def search_products(name=None, category=None, min_count=None, max_count=None):
    query = {}
    
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}  # Case-insensitive search
    if category:
        query['category'] = category
    
    products = db.items.find(query, {'_id': 0})
    return list(products)

def filter_products(criteria):
    query = {}
    
    for key, value in criteria.items():
        if key == 'name':
            query['name'] = {'$regex': value, '$options': 'i'}  # Case-insensitive search
        elif key == 'category':
            query['category'] = value
        elif key == 'price':
            query['price_per_unit'] = value  # Directly assign the price value
    
    products = db.items.find(query, {'_id': 0})
    return list(products)