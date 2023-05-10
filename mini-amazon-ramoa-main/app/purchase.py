from flask import render_template, redirect, url_for
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product
from .models.listing import Listing
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchase', __name__)

#later problem
#purchase page that contains purchase info for a given user, shows account info like balance etc., not same as home page
#can click to rediect to specific purchase pages with all order info

@bp.route('/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
    if current_user.is_authenticated:
        return redirect(url_for('product.show_product_list', page = 0))
    return render_template('user.html', user=username)

    # show the user profile for that user
    return f'User {escape(username)}'

@bp.route('/order/<order_id>', methods=['GET', 'POST'])
def show_order_page(order_id):
    if current_user.is_authenticated:
        return redirect(url_for('product.show_product_list', page = 0))
    return render_template('order.html', order=order_id)

    # show the order page for that order
    return f'Order {escape(order_id)}'
