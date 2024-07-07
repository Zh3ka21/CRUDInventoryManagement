from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from flask_login import current_user

from app.forms import OrderForm, StatusForm, csrf
from app.orders import create_order, fetch_order_history, update_order_status
from app.filters import search_products


orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/search_products', methods=['GET'])
def search_products_view():
    name = request.args.get('name')
    products = search_products(name=name, isLow=False)
    return jsonify(products)

@orders_bp.route("/create_order", methods=['GET', 'POST'])
@login_required
def create_order_view():
    form = OrderForm()
    if form.validate_on_submit():
        item_name = form.item_name.data
        quantity = form.quantity.data
        
        if create_order(item_name, quantity, current_user.email):
            return redirect(url_for('orders.create_order_view'))
        else:
            flash('Failed to create order. Please try again.', 'danger')
    
    return render_template("create_order.html", form=form)

@orders_bp.route("/orders_list", methods=['GET', 'POST'])
@login_required
def orders_list():
    orders = fetch_order_history(current_user.email)
    
    # Format dates before passing to the template
    for order in orders:
        order['order_date_formatted'] = order['order_date'].strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template("orders_list.html", orders=orders)

@orders_bp.route("/update_order", methods=['GET', 'POST'])
@login_required
def update_order_view():
    form = StatusForm()
    # Ensure the user is an admin
    if current_user.status == 'admin':
        orders = fetch_order_history(current_user.email)
        for order in orders:
            order['order_date_formatted'] = order['order_date'].strftime('%Y-%m-%d %H:%M:%S')

        # Process form submission
        if request.method == 'POST':
            order_id = request.form.get('order_id')
            status = request.form.get('status')

            # Attempt to update the order status
            if update_order_status(order_id, status):
                flash(f"Order {order_id} status updated to '{status}'.", 'success')
                return redirect(url_for('orders.update_order_view'))
            else:
                flash("Failed to update the order status. Please check the input.", 'error')

    else:
        flash("Only admin can change status", 'error')

    return render_template("update_order.html", orders=orders, form=form)