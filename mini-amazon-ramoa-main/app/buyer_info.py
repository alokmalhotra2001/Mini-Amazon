from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.public_page import PublicProfile
from .models.rating import Rating
from .models.user import User
from .models.buyerInfo import BuyerInfo

from flask import Blueprint
bp = Blueprint('buyer_info', __name__)
#This file Mimi

@bp.route('/view_buyer_info/<int:buyer_id>', methods=['GET', 'POST'])
def view_profile(buyer_id):
    # Right now, the only place that calls ID is in index.html, and ID is hard-coded as 99
    # The idea is to call public_profile whenever necessary, but plugin the appropriate ID of the user we're looking at

    # Fix if current user/future variable does not exist in DB
   
    viewing_profile = BuyerInfo.get_info(buyer_id)
    
    return render_template('buyer_info.html', profile=viewing_profile)

