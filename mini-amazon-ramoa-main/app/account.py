from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.account import Account
from .models.public_page import PublicProfile

from flask import Blueprint
bp = Blueprint('account', __name__)
#seller = Account.get_if_seller(current_user.id)

@bp.route('/your_account', methods=['GET', 'POST'])
def your_account():
    # Fix if current user/future variable does not exist in DB
    # user_history = History.get_history(current_user.id)
    user_account = Account.get_info(current_user.id)
    return render_template('account.html', account=user_account, seller=Account.get_if_seller(current_user.id))

########## COMMENT DETAILS: ##########

# All of these following functions are aptly named. They call models/account.py to update the relevant piece of info for the user
# 

@bp.route('/update_firstname', methods=['GET', 'POST'])
def update_firstname():
    firstName = request.form['first']
    flash("First name updated to " + firstName)
    return render_template('account.html', account=Account.update_first(current_user.id, firstName),seller=Account.get_if_seller(current_user.id))

@bp.route('/update_lastname', methods=['GET', 'POST'])
def update_lastname():
    lastName = request.form['last']
    flash("Last name updated to " + lastName)
    return render_template('account.html', account=Account.update_last(current_user.id, lastName),seller=Account.get_if_seller(current_user.id))

@bp.route('/update_address', methods=['GET', 'POST'])
def update_address():
    address = request.form['address']
    flash("Address updated to " + address)
    return render_template('account.html', account=Account.update_address(current_user.id, address),seller=Account.get_if_seller(current_user.id))

@bp.route('/update_password', methods=['GET', 'POST'])
def update_password():
    password = request.form['password']
    flash("Password updated to " + password)
    return render_template('account.html', account=Account.update_password(current_user.id, password),seller=Account.get_if_seller(current_user.id))

#Checks to see if email exists first, which is done in the update_email file. 
@bp.route('/update_email', methods=['GET', 'POST'])
def update_email():
    email = request.form['email']
    account=Account.update_email(current_user.id, email)

    #If the email wasn't changed (account email is unchanged following function call), email exists
    if account.email != email:
        flash("Email already belongs to a registered user.")
    else:
        flash("Email updated to " + email)
    return render_template('account.html', account=account,seller=Account.get_if_seller(current_user.id))

#If a user is not a seller, enables them to become a seller
#This function call can only be clicked on if a user is not a seller
#We did not enable the other way around (seller -> not a seller), since a seller can simply not post items anymore
@bp.route('/become_seller', methods=['GET', 'POST'])
def become_seller():
    #just in case the user somehow manages to access this link if they are a seller, exit early without changing seller status
    if Account.get_if_seller(current_user.id):
        flash("You are already a seller!")
        return render_template('account.html', account=Account.get_info(current_user.id),seller=Account.get_if_seller(current_user.id))
    
    Account.become_seller(current_user.id)
    flash("You are now a seller!")
    return render_template('account.html', account=Account.get_info(current_user.id),seller=Account.get_if_seller(current_user.id))

