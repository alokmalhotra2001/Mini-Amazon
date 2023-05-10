from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.balance import Balance

from flask import Blueprint
bp = Blueprint('balance', __name__)

# Gets the current balance on page load
@bp.route('/balance', methods=['GET', 'POST'])
def balance():
    user_balance = Balance.get_balance(current_user.id)
    return render_template('balance.html', balance=user_balance)

# On deposit form submit, increments balance by entered amount
@bp.route('/update_balance_dep', methods=['GET', 'POST'])
def update_balance_dep():
    dAmount = request.form['deposit']
    flash('You deposited $' + str(dAmount))
    return redirect(url_for('balance.balance', balance=Balance.update_balance(current_user.id, dAmount)))

# On withdrawal form submit, decrements balance by entered amount
@bp.route('/update_balance_with', methods=['GET', 'POST'])
def update_balance_with():
    forPrint = request.form['withdraw']
    wAmount = -1*(float(forPrint))  
    flash('You withdrew $' + str(forPrint))
    return redirect(url_for('balance.balance', balance=Balance.update_balance(current_user.id, wAmount)))

# Checks to see if the gift code you entered is in our DB and if so, increments balance by the amount on the card
@bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    code = request.form['gift']
    balance=Balance.verify_code(current_user.id, code)
    if balance:
        flash("You have used your code successfully!")
        return redirect(url_for('balance.balance', balance=balance))
    else:
        flash("Your code is invalid.")
        return redirect(url_for('balance.balance', balance=Balance.get_balance(current_user.id)))

# Generates new card with an amount == how much you withdraw
@bp.route('/make_code', methods=['GET', 'POST'])
def make_code():
    cardAmount = request.form['make']
    amount, code, balance=Balance.make_card(current_user.id, cardAmount)
    flash("Made a $" + "{:.2f}".format(float(amount)) + " gift card with code " + str(code))
    flash("Keep track of this code! You can use the gift card yourself or give the code to a friend to use.")
    flash("Your balance was decremented by $" + "{:.2f}".format(float(amount)))
    return redirect(url_for('balance.balance', balance=balance))