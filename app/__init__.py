from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB
from flask import current_app as app


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .product import bp as product_bp
    app.register_blueprint(product_bp)

    from .purchase import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    from .ratings import bp as rating_bp
    app.register_blueprint(rating_bp)

    # Next 3 are Rohin pages, if issues, ask rohin
    from .public_page import bp as public_bp
    app.register_blueprint(public_bp)

    from .history import bp as history_bp
    app.register_blueprint(history_bp)

    from .balance import bp as balance_bp
    app.register_blueprint(balance_bp)

    from .account import bp as account_bp
    app.register_blueprint(account_bp)
    
    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .order import bp as order_bp
    app.register_blueprint(order_bp)

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    from .seller_orders import bp as seller_orders_bp
    app.register_blueprint(seller_orders_bp)

    from .quantityTest import bp as quantityTest_bp
    app.register_blueprint(quantityTest_bp)
    
    from .seller_order_details import bp as seller_order_details_bp
    app.register_blueprint(seller_order_details_bp)
    
    from .buyer_info import bp as buyer_info_bp
    app.register_blueprint(buyer_info_bp)
    return app
