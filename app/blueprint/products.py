from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
import logging

from app.inventory_track import low_stock
from app import db

products_bp = Blueprint('products', __name__)

@products_bp.route("/manage_products", methods=['GET', 'POST'])
@login_required
def manage_products():
    if request.method == 'POST':
        if 'add_product' in request.form:
            item_name = request.form['name']
            count = int(request.form['count'])
            description = request.form['description']
            category = request.form['category']
            price = float(request.form['price_per_unit'])
            supplier = request.form['supplier']
            
            exist = db.items.find_one({"name": item_name})
            if exist:
                flash(f"Item '{item_name}' already exists in the database.", 'error')
            else:
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
                
                db.items.insert_one(item)
                logging.info(f"Item '{item_name}' added successfully.")
                low_stock(item_name)  # Assuming this function is defined elsewhere
            
        elif 'update_product' in request.form:
            item_name = request.form['update_name']
            count = int(request.form['update_count'])
            description = request.form['update_description']
            category = request.form['update_category']
            price = float(request.form['update_price_per_unit'])
            supplier = request.form['update_supplier']
            
            exist = db.items.find_one({"name": item_name})
            if exist:
                item = {
                    'name': item_name,
                    'count': count,
                    'description': description,
                    'category': category,
                    'updated_at': datetime.now(),
                    'price_per_unit': price,
                    'supplier': [supplier]
                }
                
                db.items.update_one({'_id': exist['_id']}, {'$set': item})
                logging.info(f"Item '{item_name}' updated successfully.")
                
                # TODO: CHECK THIS
                low_stock(item_name)  # Assuming this function is defined elsewhere
            else:
                flash(f"Item with name '{item_name}' does not exist.", 'error')
            
        elif 'delete_product' in request.form:
            item_name = request.form['delete_name']
            
            exist = db.items.find_one({"name": item_name})
            if exist:
                db.items.delete_one({'_id': exist['_id']})
                logging.info(f"Item '{item_name}' deleted successfully.")
            else:
                flash(f"Item '{item_name}' does not exist in the database.", 'error')
            
        return redirect(url_for('products.manage_products'))

    search_name = request.args.get('search_name')
    if search_name:
        products = list(db.items.find({"name": {"$regex": search_name, "$options": "i"}}))
    else:
        products = None
        
    return render_template('manage_products.html', products=products)


