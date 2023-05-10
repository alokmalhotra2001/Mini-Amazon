from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('quantityTest', __name__)


@bp.route('/quantity/<int:listing_id>', methods=['GET', 'POST'])
def quantity(listing_id):
    currQuantity = Inventory.get_quantity(listing_id)
    return render_template('quantity.html', quantity=currQuantity)


@bp.route('/change_quantity_to/<int:listing_id>', methods=['GET','POST'])
def change_quantity_to(listing_id):
    new_quantity= request.form['quantityform']
    old_quantity = Inventory.get_quantity(listing_id)
    return render_template('quantity.html', quantity=Inventory.change_quantity(old_quantity, new_quantity, current_user.id, listing_id))
