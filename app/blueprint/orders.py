from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

from app.orders import create_order
from app.filters import search_products

orders_bp = Blueprint('orders', __name__)
csrf = CSRFProtect()

# Sample form definition using Flask-WTF
class OrderForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

@orders_bp.route('/search_products', methods=['GET'])
def search_products_view():
    name = request.args.get('name')
    # Assuming search_products is defined elsewhere to fetch products
    products = search_products(name=name, isLow=False)
    return jsonify(products)

@orders_bp.route("/create_order", methods=['GET', 'POST'])
@login_required
@csrf.exempt 
def create_order_view():
    form = OrderForm()
    if form.validate_on_submit():
        item_name = form.item_name.data
        quantity = form.quantity.data
        email = form.email.data
        
        # Assuming create_order function is defined elsewhere
        if create_order(item_name, quantity, email):
            return redirect(url_for('orders.create_order_view'))
        else:
            flash('Failed to create order. Please try again.', 'danger')
    
    return render_template("create_order.html", form=form)
