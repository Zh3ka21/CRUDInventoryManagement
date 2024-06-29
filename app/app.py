from flask import Flask, render_template
from blueprint.auth import auth_bp
from blueprint.inventory import inventory_bp
from blueprint.orders import orders_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(inventory_bp, url_prefix='/inventory')
    # app.register_blueprint(orders_bp, url_prefix='/orders')

    @app.route('/home')
    def home():
        return render_template('base.html')

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/about')
    def about():
        return render_template('dashboard.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
