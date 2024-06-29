from flask import Blueprint, render_template, request, flash, redirect, url_for

orders_bp = Blueprint('orders', __name__)
from orders import create_order, fetch_order_history, update_order_status

@orders_bp.route('/orders', methods=['GET', 'POST'])
def orders_view():
    if request.method == 'POST':
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])
        email = request.form['email']
        create_order(item_name, quantity, email)
        flash('Order created successfully!', 'success')
    orders = fetch_order_history()
    return render_template('orders.html', orders=orders)



@orders_bp.route('/update', methods=['POST'])
def update_order_view():
    order_id = request.form['order_id']
    new_status = request.form['new_status']
    update_order_status(order_id, new_status)
    flash('Order status updated successfully!', 'success')
    return redirect(url_for('orders.orders_view'))
