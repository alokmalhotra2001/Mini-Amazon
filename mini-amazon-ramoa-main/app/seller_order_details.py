from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_babel import _, lazy_gettext as _l
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional

from .models.user import User
from .models.history import History
from .models.order import Order
from .models.seller_order_details import SellerOrderDetails
from .models.seller_orders import SellerOrders

from flask import Blueprint
bp = Blueprint('seller_order_details', __name__)

# Show order details for a particular order
@bp.route('/your_inventory/your_seller_orders/<o_id>', methods=['GET', 'POST'])
def show_order_details(o_id):
    details = SellerOrderDetails.get_order(o_id, current_user.id)
    order_total_price = 0

    for item in details:
        
        item_price_float = round(item.price, 2)
        item.price = "{:.2f}".format(item_price_float)
        
        item_subtotal_float = round(item.quantity * item_price_float, 2)
        item.subtotal = "{:.2f}".format(item_subtotal_float)

        order_total_price += item_subtotal_float

    order_total_price = round(order_total_price, 2)
    order_tot = "{:.2f}".format(order_total_price)

    buyer_side = False

    return render_template('seller_order_details.html', order_id = o_id, od = details, total = order_tot, buyer_side=buyer_side)

# @bp.route('/your_inventory/your_seller_orders/<o_id>/fulfill/<l_id>', methods=['POST','GET'])
# def fulfill_order(o_id,l_id):
#     response = SellerOrderDetails.fulfill_order(o_id, l_id)
#     order_details = SellerOrderDetails.get_order(o_id, current_user.id)
#     order_fulfilled = True
#     for item in order_details:
#         print(item)
#         item_fulfilled = item.fulfilled
#         print(item.fulfilled)
#         if not item_fulfilled:
#             order_fulfilled = False 
#     if order_fulfilled:
#         print("FULFILL THIS MF ORDER")
#         print(SellerOrders.fulfill_whole_order(o_id))
#     print(response)
#     return show_order_details(o_id)

@bp.route('/your_inventory/your_seller_orders/<o_id>/fulfill/<l_id>', methods=['POST','GET'])
def fulfill_order(o_id,l_id):
    response = SellerOrderDetails.fulfill_order(o_id, l_id)
    order_details = SellerOrderDetails.get_order(o_id, current_user.id)
    order_fulfilled = 1
    for item in order_details:
        if (item.fulfilled == '0'):
            order_fulfilled = 0
            break
        else: 
            continue
    if (order_fulfilled == 1):
        x = SellerOrders.fulfill_whole_order(o_id)
    return show_order_details(o_id)
