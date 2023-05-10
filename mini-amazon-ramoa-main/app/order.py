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

from flask import Blueprint
bp = Blueprint('order', __name__)

# Show order details for a particular order
@bp.route('/your_history/order/<o_id>', methods=['GET', 'POST'])
def show_order_details(o_id):
    details = Order.get_order(o_id)
    order_total_price = 0

    for item in details:
        if (item.fulfilled == '0'):
            item.fulfilled = 'Pending Seller Fulfillment'
            item.datetime_fulfilled = 'N/A'
        else:
            item.fulfilled = 'Item Fulfilled by Seller'

        item_price_float = round(item.price, 2)
        item.price = "{:.2f}".format(item_price_float)
        
        item_subtotal_float = round(item.quantity * item_price_float, 2)
        item.subtotal = "{:.2f}".format(item_subtotal_float)

        order_total_price += item_subtotal_float

    order_total_price = round(order_total_price, 2)
    order_tot = "{:.2f}".format(order_total_price)

    buyer_side = True

    return render_template('order_details.html', order_id = o_id, od = details, total = order_tot, buyer_side=buyer_side)
