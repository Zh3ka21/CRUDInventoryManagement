from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.forms.main_forms import ProductForm
from app.products import add_product, update_product, delete_product, get_all_products
from app.filters import search_products
from .utils import sort_products
from app.inventory_track import fetch_stocks
from app.filters import search_products
from bson import ObjectId
from flask_wtf.csrf import CSRFProtect
from app import db


csrf = CSRFProtect()
products_bp = Blueprint('products', __name__)

@products_bp.route("/products", methods=['GET'])
@login_required
def manage_products():
    search_name = request.args.get('search_name')
    if search_name:
        products = list(search_products(search_name))
    else:
        products = get_all_products()
    return render_template('manage_products.html', products=products, add_form=ProductForm())

@products_bp.route("/products/add", methods=['GET'])
@login_required
def add_product_form():
    return render_template('add_product.html', form=ProductForm())

@products_bp.route("/products", methods=['POST'])
@login_required
def add_product_view():
    form = ProductForm()
    if form.validate_on_submit():
        add_product(
            form.item_name.data,
            form.count.data,
            form.description.data,
            form.category.data,
            form.price_per_unit.data,
            form.supplier.data
        )
        flash('Product added successfully', 'success')
    else:
        flash('Error adding product', 'danger')
    return redirect(url_for('products.manage_products'))

@products_bp.route("/products/edit/<product_id>", methods=['GET'])
@login_required
def edit_product_view(product_id):
    product = db.items.find_one(ObjectId(product_id))
    form = ProductForm(obj=product)
    return render_template('edit_product.html', form=form, product=product)


@products_bp.route("/products/update/<product_id>", methods=['POST'])
@login_required
def update_product_view(product_id):
    form = ProductForm()
    _id = ObjectId(product_id)
    if form.validate_on_submit():
        update_product(
            _id,
            form.item_name.data,
            form.count.data,
            form.description.data,
            form.category.data,
            form.price_per_unit.data,
            form.supplier.data
        )
        flash('Product updated successfully', 'success')
    else:
        flash('Error updating product', 'danger')
    return redirect(url_for('products.manage_products'))

# SO that to fix an error with method not FOUND
#from werkzeug.middleware.http_method_override import HTTPMethodOverrideMiddleware
#app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

@products_bp.route("/products/<product_id>", methods=['DELETE', 'POST'])
@login_required
def delete_product_view(product_id):
    delete_product(ObjectId(product_id))
    flash('Product deleted successfully', 'success')
    return redirect(url_for('products.manage_products'))


@products_bp.route("/product_details", methods=['GET', 'POST'])
@login_required
def product_details():
    sort_by = request.args.get('sort_by', 'item_name')
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