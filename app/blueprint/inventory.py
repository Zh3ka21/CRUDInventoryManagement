from flask import Blueprint, render_template

inventory_bp = Blueprint('inventory', __name__)
from app.inventory_track import fetch_stocks

@inventory_bp.route('/inventory')
def inventory_view():
    items = fetch_stocks()
    return render_template('inventory.html', items=items)
