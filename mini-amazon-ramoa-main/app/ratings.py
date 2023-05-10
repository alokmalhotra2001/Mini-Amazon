from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from flask_babel import _, lazy_gettext as _l
from datetime import datetime

from .models.user import User
from .models.rating import Rating
from .models.rating import Message

from flask import Blueprint
bp = Blueprint('ratings', __name__)

# Displays all reviews written by a registered users
@bp.route('/your_reviews/<start>', methods=['GET', 'POST'])
def your_reviews(start):
    start = int(start)
    next_start = start + 10
    prev_start = start - 10

    p_reviews = Rating.p_ratings_from_user(current_user.id, start)
    s_reviews = Rating.s_ratings_from_user(current_user.id, start)

    print("Length p_reviews:" + str(len(p_reviews)))
    print("Length s_reviews:" + str(len(s_reviews)))

    if len(p_reviews) == 0 and len(s_reviews) == 0:
        if prev_start < 0:
            prev_start = 0
        return render_template('no_older_reviews.html', prev_start=prev_start)
    
    return render_template('your_reviews.html', product_reviews=p_reviews, seller_reviews=s_reviews, place=next_start)

# Form to edit review
class EditForm(FlaskForm):
    rating = RadioField(_l('Rating'), validators=[DataRequired()], choices=[0, 1, 2, 3, 4, 5])
    review = StringField(_l('Review'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Review'))

# Page to edit product reviews
@bp.route('/edit_product_review/<reviewer>/<reviewee>/<rating>/<review>/<start>/<l_id>', methods=['GET', 'POST'])
def edit_product_review(reviewer, reviewee, rating, review, start, l_id):
    form = EditForm()
    if form.validate_on_submit():
        print(len(form.review.data))
        print(type(form.review.data))
        if Rating.update_product_rating(reviewer, reviewee, form.rating.data, form.review.data):
            if int(l_id) < 0:
                return redirect(url_for('ratings.your_reviews', start=start))
            return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))
    
    return render_template('edit_product_review.html', title='Edit Product Review', rating=rating, review=review, reviewee=reviewee, form=form, l_id=int(l_id), start=start)

# Page to edit seller reviews
@bp.route('/edit_s_review/<reviewer>/<reviewee>/<rating>/<review>/<start>', methods=['GET', 'POST'])
def edit_s_review(reviewer, reviewee, rating, review, start):
    form = EditForm()
    if form.validate_on_submit():
        if Rating.update_seller_rating(reviewer, reviewee, form.rating.data, form.review.data):
            return redirect(url_for('ratings.your_reviews', start=start))
    
    return render_template('edit_review.html', title='Edit Review', rating=rating, review=review, form=form, start=start)

@bp.route('/edit_s_review_public/<reviewer>/<reviewee>/<rating>/<review>/<start>', methods=['GET', 'POST'])
def edit_s_review_public(reviewer, reviewee, rating, review, start):
    form = EditForm()
    if form.validate_on_submit():
        if Rating.update_seller_rating(reviewer, reviewee, form.rating.data, form.review.data):
            return redirect(url_for('public_page.view_profile', start=start, ID=reviewee))

    return render_template('edit_s_review_public.html', title='Edit Review Public', rating=rating, review=review, form=form, start=start, reviewee=reviewee)   

# Deletes product reviews and reroutes to page of origin
@bp.route('/delete_p_review/<reviewer>/<reviewee>/<start>/<l_id>', methods=['GET', 'POST'])
def delete_product_review(start, reviewer, reviewee, l_id):
    Rating.delete_product_rating(reviewer, reviewee)

    if int(l_id) < 0:
        return redirect(url_for('ratings.your_reviews', start=start))
    
    return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))

# Deletes seller reviews and reroutes to page of origin
@bp.route('/delete_seller_review/<reviewer>/<reviewee>/<start>/<came_from>/<o_id>', methods=['GET', 'POST'])
def delete_seller_review(start, reviewer, reviewee, came_from, o_id):
    if Rating.get_your_s_review(current_user.id, reviewee) is not None:
        Rating.delete_seller_rating(reviewer, reviewee)

    came_from = int(came_from)
    
    if came_from == 1:
        return redirect(url_for('ratings.your_reviews', start=start))
    elif came_from == 2:
        return redirect(url_for('public_page.view_profile', start=start, ID=reviewee))
    elif came_from == 3:
        return redirect(url_for('order.show_order_details', o_id=o_id))   

# Shows all reviews left for a product
@bp.route('/show_product_reviews/<reviewee>/<l_id>/<start>', methods=['GET','POST'])
def show_product_reviews(reviewee, l_id, start):
    reviewee = int(reviewee)
    start = int(start)
    
    review_count, avg_rating = Rating.product_summary(reviewee)

    your_rating = None
    other_ratings = Rating.other_product_ratings(reviewee, start)
    top_ratings = Rating.get_top_p_reviews(reviewee)

    if current_user.is_authenticated:
        your_rating = Rating.get_your_p_review(current_user.id, reviewee)
        other_ratings = Rating.other_product_ratings(reviewee, start, current_user.id)
    
    if len(other_ratings) == 0:
        prev_start = start - 10
        if prev_start < 0:
            prev_start = 0
        return render_template('no_older_p_reviews.html', count=review_count, avg=avg_rating, your_rating=your_rating, others=other_ratings, start=start, reviewee=reviewee, l_id=l_id, prev_start=prev_start, top_ratings=top_ratings)
    
    return render_template('product_reviews.html', count=review_count, avg=avg_rating, your_rating=your_rating, others=other_ratings, start=start, reviewee=reviewee, l_id=l_id, top_ratings=top_ratings)

# Form to create new reviews
class CreateForm(FlaskForm):
    rating = RadioField(_l('Rating'), validators=[DataRequired()], choices=[0, 1, 2, 3, 4, 5])
    review = StringField(_l('Review'), validators=[DataRequired()])
    submit = SubmitField(_l('Create Review'))

# Page to add product reviews
@bp.route('/add_p_review/<reviewer>/<reviewee>/<start>/<l_id>', methods=['GET','POST'])
def add_p_review(reviewer, reviewee, start, l_id):
    form = CreateForm()
    if form.validate_on_submit():
        dateAndTime = datetime.now()
        if Rating.add_p_rating(reviewer, reviewee, form.rating.data, dateAndTime, form.review.data):
            return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))
    
    return render_template('add_p_review.html', title='Edit Review', form=form, reviewee=reviewee, start=start, l_id=l_id)

# Page to add reviews of a seller via their public page
@bp.route('/add_s_review_public/<reviewer>/<reviewee>/<start>', methods=['GET','POST'])
def add_s_review_public(reviewer, reviewee, start):
    form = CreateForm()
    if form.validate_on_submit():
        dateAndTime = datetime.now()
        if Rating.add_s_rating(reviewer, reviewee, form.rating.data, dateAndTime, form.review.data):
            return redirect(url_for('public_page.view_profile', start=start, ID=reviewee))
    
    return render_template('add_s_review_public.html', title='Edit Review', form=form, reviewee=reviewee, start=start)

# Page to add or edit reviews of a seller through your detailed order page
@bp.route('/add_s_review_order/<reviewer>/<reviewee>/<o_id>', methods=['GET','POST'])
def add_s_review_order(reviewer, reviewee, o_id):
    your_rating = Rating.get_your_s_review(current_user.id, reviewee)
    if your_rating is None:
        form = CreateForm()
        if form.validate_on_submit():
            dateAndTime = datetime.now()
            if Rating.add_s_rating(reviewer, reviewee, form.rating.data, dateAndTime, form.review.data):
                return redirect(url_for('order.show_order_details', o_id=o_id))
        
        return render_template('add_s_review_order.html', title='Add Review', form=form, reviewee=reviewee, o_id=o_id)
    else:
        form = EditForm()
        if form.validate_on_submit():
            if Rating.update_seller_rating(reviewer, reviewee, form.rating.data, form.review.data):
                return redirect(url_for('order.show_order_details', o_id=o_id))

        return render_template('edit_s_review_order.html', title='Edit Review', rating=your_rating.rating, review=your_rating.review, form=form, o_id=o_id)

@bp.route('/add_like/<reviewer>/<reviewee>/<action>/<l_id>/<start>', methods=['GET','POST'])
def add_like(reviewer, reviewee, action, l_id, start):
    can_like, update = Rating.can_like_p_review(reviewer, reviewee, current_user.id, action)

    if can_like:
        dateAndTime = datetime.now()
        success = Rating.like_p_review(reviewer, reviewee, current_user.id, action, dateAndTime, update)

    return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))

@bp.route('/remove_like/<reviewer>/<reviewee>/<l_id>/<start>', methods=['GET','POST'])
def remove_like(reviewer, reviewee, l_id, start):
    Rating.remove_p_review_like(reviewer, reviewee, current_user.id)
    return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))

# Form to add messages
class MessageForm(FlaskForm):
    message = TextAreaField(_l('New Message'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

# Page that displays all messages between you and a seller you've purchased from
@bp.route('/view_messages/<l_id>/<o_id>/<buyer_side>', methods=['GET','POST'])
def view_messages(l_id, o_id, buyer_side):
    message_thread = Message.get_messages(o_id, l_id)
    buyer_side = eval(buyer_side)

    form = MessageForm()
    if form.validate_on_submit():
        dateAndTime = datetime.now()
        if Message.add_message(o_id, current_user.id, l_id, form.message.data, dateAndTime):
            return redirect(url_for('ratings.view_messages', l_id=l_id, o_id=o_id, buyer_side=buyer_side))
    
    return render_template('messages.html', messages=message_thread, form=form, o_id=o_id, buyer_side=buyer_side)


