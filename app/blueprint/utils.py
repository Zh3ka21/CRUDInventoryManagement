def sort_products(products, sort_by, order):
    if sort_by == 'item_name':
        key = lambda x: x.get('item_name', '').lower()  # Access 'name' from dictionary safely
    elif sort_by == 'count':
        key = lambda x: x.get('count', 0)  # Access 'count' from dictionary safely
    elif sort_by == 'category':
        key = lambda x: x.get('category', '').lower()  # Access 'category' from dictionary safely
    elif sort_by == 'price_per_unit':
        key = lambda x: x.get('price_per_unit', 0.0)  # Access 'price_per_unit' from dictionary safely
    elif sort_by == 'supplier':
        key = lambda x: x.get('supplier', '').lower()  # Access 'supplier' from dictionary safely
    else:
        # Default sorting by name if sort_by parameter is unrecognized
        key = lambda x: x.get('name', '').lower()

    sorted_products = sorted(products, key=key, reverse=(order == 'desc'))
    return sorted_products

def convert_ids_to_str(orders: list):
    for di in orders:
        for k, v in di.items():
            if k == '_id':
                di[k] = str(v)
    return list(orders)