##RECENTLY DEPRECATED:
@bp.route('/delete_p_review/<reviewer>/<reviewee>/<start>', methods=['GET', 'POST'])
def delete_p_review(start, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_product_rating(reviewer, reviewee)

    return redirect(url_for('ratings.your_reviews', start=start))

@bp.route('/delete_p_review_dpp/<reviewer>/<reviewee>/<start>/<l_id>', methods=['GET', 'POST'])
def delete_p_review_dpp(start, l_id, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_product_rating(reviewer, reviewee)

    return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))

@bp.route('/delete_s_review/<reviewer>/<reviewee>/<start>', methods=['GET', 'POST'])
def delete_s_review(start, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_seller_rating(reviewer, reviewee)
        
    return redirect(url_for('ratings.your_reviews', start=start))

@bp.route('/delete_s_review_public/<reviewer>/<reviewee>/<start>', methods=['GET', 'POST'])
def delete_s_review_public(start, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_seller_rating(reviewer, reviewee)
        
<<<<<<< HEAD
    return redirect(url_for('public_page.your_profile', start=start))
=======
    return redirect(url_for('public_page.view_profile', start=start))
>>>>>>> e58e45b62a2b97b197684c96b9b44d19a540d1cb


####
#######--------DEPRECATED CODE-------##########
@bp.route('/delete_p_review/<reviewer>/<reviewee>/<start>', methods=['GET', 'POST'])
def delete_p_review(start, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_product_rating(reviewer, reviewee)

    return redirect(url_for('ratings.your_reviews', start=start))

@bp.route('/delete_p_review_dpp/<reviewer>/<reviewee>/<start>/<l_id>', methods=['GET', 'POST'])
def delete_p_review_dpp(start, l_id, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_product_rating(reviewer, reviewee)

    return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))

@bp.route('/delete_s_review/<reviewer>/<reviewee>/<start>', methods=['GET', 'POST'])
def delete_s_review(start, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_seller_rating(reviewer, reviewee)
        
    return redirect(url_for('ratings.your_reviews', start=start))

@bp.route('/delete_s_review_public/<reviewer>/<reviewee>/<start>', methods=['GET', 'POST'])
def delete_s_review_public(start, reviewer=None, reviewee=None):
    #if reviewer is not None and reviewee is not None:
    Rating.delete_seller_rating(reviewer, reviewee)
        
<<<<<<< HEAD
    return redirect(url_for('public_page.your_profile', start=start))
=======
    return redirect(url_for('public_page.view_profile', start=start))
>>>>>>> e58e45b62a2b97b197684c96b9b44d19a540d1cb

@bp.route('/edit_p_review/<reviewer>/<reviewee>/<rating>/<review>/<start>', methods=['GET', 'POST'])
def edit_p_review(reviewer, reviewee, rating, review, start):
    form = EditForm()
    if form.validate_on_submit():
        if Rating.update_product_rating(reviewer, reviewee, form.rating.data, form.review.data):
            return redirect(url_for('ratings.your_reviews', start=start))
    
    return render_template('edit_review.html', title='Edit Review', rating=rating, review=review, form=form, start=start)

@bp.route('/edit_p_review_dpp/<reviewer>/<reviewee>/<rating>/<review>/<start>/<l_id>', methods=['GET', 'POST'])
def edit_p_review_dpp(reviewer, reviewee, rating, review, start, l_id):
    form = EditForm()
    if form.validate_on_submit():
        if Rating.update_product_rating(reviewer, reviewee, form.rating.data, form.review.data):
            #return redirect(url_for('ratings.your_reviews', start=start))
            return redirect(url_for('ratings.show_product_reviews', reviewee=reviewee, l_id=l_id, start=start))
    
    return render_template('edit_review_dpp.html', title='Edit Review DPP', rating=rating, review=review, reviewee=reviewee, form=form, l_id=l_id, start=start)


