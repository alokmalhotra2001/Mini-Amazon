from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.listing import Listing
from .models.product import Product
from .models.purchase import Purchase
from .models.rating import Rating
from .models.inventory import Inventory
from .models.seller_orders import SellerOrders
from flask import Blueprint
bp = Blueprint('seller_orders', __name__)

# show all orders belonging to logged in seller
@bp.route('/your_seller_orders/', methods=['GET', 'POST'])
def show_seller_orders():
    orders = SellerOrders.get_seller_orders(current_user.id)
    return render_template('your_seller_orders.html', seller_orders=orders)

# show all orders belonging to logged in seller, can filter and sort
@bp.route('/your_seller_orders/<string:query_id>', methods=['GET', 'POST'])
def show_sort_seller_orders(query_id):
    orders = SellerOrders.get_seller_orders(current_user.id)
    #product = Inventory.get(product_id)
    # if something gets passed into the form, redirct to the query list 
    # else display products
    # return str(products)
     # Try to query the information from the sort checkbox, try and if it doesn't work set it to empty
    try:
        sort = str(request.form['sort'])
    except:
        sort = ''

    # Try to query the information from the filter checkbox, try and if it doesn't work set it to empty
    try:
        filter = str(request.form['filter'])
    except:
        filter = ''
    if sort or filter:
        query_id = sort+filter
        return redirect(url_for('seller_orders.show_sort_seller_orders', query_id=query_id))
    if query_id == 'temp':
        return redirect(url_for('seller_orders.show_seller_orders'))
    if query_id == '':
        # query_id doesn't exist, redirect to generic orders page
        return redirect(url_for('seller_orders.show_seller_orders'))

    if query_id == 'pa':
        orders = SellerOrders.get_all_seller_orders_asc(current_user.id)
    elif query_id == 'of':
        orders = SellerOrders.get_orders_fulfilled(current_user.id)
    elif query_id == 'ou':
        orders = SellerOrders.get_orders_unfulfilled(current_user.id)

    return render_template('your_seller_orders.html', seller_orders=orders)
