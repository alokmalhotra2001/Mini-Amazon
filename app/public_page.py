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

from flask import Blueprint
bp = Blueprint('public_page', __name__)
#This file Mimi

@bp.route('/view_profile/<start>/<ID>', methods=['GET', 'POST'])
def view_profile(start, ID):
    # Right now, the only place that calls ID is in index.html, and ID is hard-coded as 99
    # The idea is to call public_profile whenever necessary, but plugin the appropriate ID of the user we're looking at

    # Fix if current user/future variable does not exist in DB
    seller = PublicProfile.get_if_seller(ID)
    viewing_profile = PublicProfile.get_info(ID)
    start = int(start)

    #add "reviewee" param to func for person whose profile you're viewing, current current_user.id is hardcoded in for reviewee
    #reviewee = int(reviewee)
    #review_count, avg_rating = Rating.seller_summary(reviewee)
    review_count, avg_rating = Rating.seller_summary(ID)

    your_rating = None
    #other_ratings = Rating.other_seller_ratings(reviewee, 0)
    other_ratings = Rating.other_seller_ratings(ID, start)

    if current_user.is_authenticated:
        #comment back in once actual seller id is accessible, currently "1" hardcoded in for reviewee
        #your_rating = Rating.get_your_s_review(current_user.id, reviewee)
        #other_ratings = Rating.other_seller_ratings(reviewee, 0, current_user.id)
        #can_review = Rating.can_review_seller(current_user.id, reviewee)
        your_rating = Rating.get_your_s_review(current_user.id, ID)
        other_ratings = Rating.other_seller_ratings(ID, start, current_user.id)
        can_review = Rating.can_review_seller(current_user.id, ID)
    
    end = False 
    if len(other_ratings) == 0:
        end = True
    
    # add in reviewee param
    return render_template('public_page.html', profile=viewing_profile, seller=seller, count=review_count, avg=avg_rating, your_rating=your_rating, others=other_ratings, can_review=can_review, start=start, end=end)

