from flask import redirect, render_template, url_for
from app.forms.main_forms import ProductForm
from app.products import get_all_products
from app.blueprint.auth import auth_bp
from app.blueprint.inventory import inventory_bp
from app.blueprint.orders import orders_bp
from app.blueprint.products import products_bp
from app.blueprint.reports import reports_bp

from app import app


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(reports_bp, url_prefix='/reports')

@app.route('/home')
def home():
   products = get_all_products()
   return render_template('base.html', products=products)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

