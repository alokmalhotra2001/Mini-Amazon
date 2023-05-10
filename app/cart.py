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
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)

# Show all items in a user's cart
@bp.route('/my-cart/<msg>', methods=['GET', 'POST'])
def show_cart(msg):
    all_items = Cart.get_cart(current_user.id)
    cart_items = []
    sfl_items = []

    for item in all_items:
        if (item.status == '1'):
            cart_items.append(item)
        else :
            sfl_items.append(item)

    cart_total_price = 0
    
    for item in cart_items:
        item_price_float = round(item.price, 2)
        item.price = "{:.2f}".format(item_price_float)

        item_subtotal_float = round(item.quantity * item_price_float, 2)
        item.subtotal = "{:.2f}".format(item_subtotal_float)
        
        cart_total_price += item_subtotal_float

    cart_total_price = round(cart_total_price, 2)
    cart_tot = "{:.2f}".format(cart_total_price)

    return render_template('cart.html', my_cart = cart_items, cart_sz = len(cart_items), my_sfl = sfl_items, sfl_sz = len(sfl_items), total = cart_tot, msg = msg)

# Edit quantity of an item in a user's cart
@bp.route('/my-cart/edit/<l_id>', methods=['GET', 'POST'])
def edit_item_quantity(l_id):
    new_quant = request.form.get("new_quant_" + str(l_id))
    if (Cart.update_item_quantity(current_user.id, l_id, new_quant) == 1):
        return redirect(url_for('cart.show_cart', msg=0))

    return redirect(url_for('cart.show_cart', msg=0))

# Remove item from user's cart
@bp.route('/my-cart/remove/<l_id>', methods=['GET', 'POST'])
def remove_item(l_id):
    if (Cart.remove_item(current_user.id, l_id) == 1):
        return redirect(url_for('cart.show_cart', msg=0))
    
    return redirect(url_for('cart.show_cart', msg=0))

# Remove all items from user's cart
@bp.route('/my-cart/remove-all', methods=['GET', 'POST'])
def remove_all():
    if (Cart.empty_cart(current_user.id) == 1):
        return redirect(url_for('cart.show_cart', msg=0))
    
    return redirect(url_for('cart.show_cart', msg=0))

@bp.route('/my-cart/place-order', methods=['GET', 'POST'])
def place_order():
    x = Cart.place_order(current_user.id)
    if (x == 'Success'):
        return redirect(url_for('cart.show_cart', msg=0))
    if ( x.startswith('ERROR (INSUFFICIENT FUNDS)') or x.startswith('ERROR (QUANTITY INVALID)') ):
        return redirect(url_for('cart.show_cart', msg=x))
    
    # if (Cart.place_order(current_user.id) == 'Success'):
    #     return redirect(url_for('cart.show_cart'))
    
    # return redirect(url_for('cart.show_cart'))

# Move item from cart to saved for later (by changing status bit to 0)
@bp.route('/my-cart/move-to-sfl/<l_id>', methods=['GET', 'POST'])
def move_sfl(l_id):
    if (Cart.move_to_sfl(current_user.id, l_id) == 1):
        return redirect(url_for('cart.show_cart', msg=0))
    
    return redirect(url_for('cart.show_cart', msg=0))


# Move item from saved for later to cart (by changing status bit to 1)
@bp.route('/my-cart/move-to-cart/<l_id>', methods=['GET', 'POST'])
def move_cart(l_id):
    if (Cart.move_to_cart(current_user.id, l_id) == 1):
        return redirect(url_for('cart.show_cart', msg=0))
    
    return redirect(url_for('cart.show_cart', msg=0))


# # Show all items in a user's cart
# @bp.route('/my-cart', methods=['GET', 'POST'])
# def show_cart():
#     cart_items = Cart.get_cart(current_user.id)
    
#     sfl_items = []

#     cart_total_price = 0

#     for item in cart_items:
#         item_price_float = round(item.price, 2)
#         item.price = "{:.2f}".format(item_price_float)

#         item_subtotal_float = round(item.quantity * item_price_float, 2)
#         item.subtotal = "{:.2f}".format(item_subtotal_float)
        
#         if (item.status == '1'):
#             cart_total_price += item_subtotal_float

#     cart_total_price = round(cart_total_price, 2)
#     cart_tot = "{:.2f}".format(cart_total_price)

#     for item in cart_items:
#         if (item.status == '0'):
#             sfl_items.append(item)
#             cart_items.remove(item)

#     return render_template('cart.html', my_cart = cart_items, my_sfl = sfl_items, total = cart_tot)
