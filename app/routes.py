from flask import render_template
from app.blueprint.auth import auth_bp
from app.blueprint.inventory import inventory_bp
from app.blueprint.orders import orders_bp

from app import app


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(orders_bp, url_prefix='/orders')

@app.route('/home')
def home():
    return render_template('base.html')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('dashboard.html')

