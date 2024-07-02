from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.products import add_product, update_product, delete_product
from app.filters import search_products
from .utils import sort_products
from app.inventory_track import fetch_stocks

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
            
            if count < 0:
                flash('Count cannot be less than zero!', 'error')
                return redirect(url_for('products.manage_products'))
            
            add_product(
                item_name,
                count,
                description,
                category,
                price,
                supplier                
            )
                        
        elif 'update_product' in request.form:
            item_name = request.form['update_name']
            count = int(request.form['update_count'])
            description = request.form['update_description']
            category = request.form['update_category']
            price = float(request.form['update_price_per_unit'])
            supplier = request.form['update_supplier']
            
            if count < 0:
                flash('Count cannot be less than zero!', 'error')
                return redirect(url_for('products.manage_products'))

            
            update_product(
                item_name,
                count,
                description,
                category,
                price,
                supplier               
            )
                        
        elif 'delete_product' in request.form:
            item_name = request.form['delete_name']
            delete_product(item_name)

        return redirect(url_for('products.manage_products'))

    search_name = request.args.get('search_name')
    if search_name:
        products = list(search_products(search_name))
    else:
        products = None
        
    return render_template('manage_products.html', products=products)


@products_bp.route("/product_details", methods=['GET', 'POST'])
@login_required
def product_details():
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    
    products = search_products(isLow=False)
    sorted_products = sort_products(products, sort_by, order)
    
    return render_template('products_details.html', sorted_products=sorted_products, sort_by=sort_by, order=order)

@products_bp.route("/below_stocks", methods=['GET', 'POST'])
@login_required
def below_stocks():
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    
    products = fetch_stocks()
    sorted_products = sort_products(products, sort_by, order)
    
    return render_template('below_stocks.html', sorted_products=sorted_products, sort_by=sort_by, order=order)