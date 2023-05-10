from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.history import History

# from .models.rating import Rating //needed for rating routes

from flask import Blueprint
bp = Blueprint('history', __name__)

@bp.route('/your_history', methods=['GET', 'POST'])
def your_history():
    # Fix if current user/future variable does not exist in DB
    # user_history = History.get_history(current_user.id)
    user_history = History.get_history(current_user.id)
    print(user_history)
    return render_template('history.html', history=user_history)
