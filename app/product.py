from flask import render_template, redirect, url_for, request, flash
from flask.ctx import copy_current_request_context
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from werkzeug.urls import url_parse
from flask_wtf.form import FlaskForm
from flask import Markup
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from app.models.cart import Cart
from app.models.inventory import Inventory
from app.models.tags import ListingsHaveTags, ListingWithTags, Tags
from .db import DB

from app.models.public_page import PublicProfile

from .models.user import User
from .models.product import Product
from .models.listing import Listing
from .models.product import Product
from .models.rating import Rating

from flask import Blueprint
bp = Blueprint('product', __name__)

# Take in an integer and return the image given the rating
def get_rpic(rpicV):
    if rpicV == 0:
        return '../static/css/images/0stars.png'
    elif rpicV == 1:
        return '../static/css/images/1stars.png'
    elif rpicV == 2:
        return '../static/css/images/2stars.png'
    elif rpicV == 3:
        return '../static/css/images/3stars.png'
    elif rpicV == 4:
        return '../static/css/images/4stars.png'
    elif rpicV == 5:
        return '../static/css/images/5stars.png'

# show all products with buttons to product pages, can search but this page is for when there is no search
# that has occured yet. 
@bp.route('/products/<int:page>', methods=['GET', 'POST'])
def show_product_list(page):
    page = int(page)
    start = int(page*20)
    # page # is start/20
    products = []
    products = Listing.get_all_listings_ln(start=start, query='')

    listings = []

    # for each product get the tags associated to display, as well as the rating information for the given
    # product id. Iterates through all listings and gets the rating, picture, and tags through query and 
    # creates objects to display them.
    for product in products:
        rsummary = Rating.product_summary(product.product_id) 

        # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
        # rating and the image of the stars.

        if rsummary[1] == "N/A" or rsummary[1] is None:
            rating = "N/A"
            rpic = '../static/css/images/0stars.png'
        else:
            rating = round(rsummary[1], 2)
            rpicV = int(round(rating))
            rpic = get_rpic(rpicV)

        p_info = Product.get_product_info(product.product_id)
        p_name = p_info.p_name

        l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
        tag_list = []
        for row in l_tag_pairs:
            tag_list.append(row.tag)
        if not tag_list:
            tag_list_f = ""
        else:
            tag_list_f = ", ".join(tag_list)
        list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
        product_id=product.product_id,listing_name=product.listing_name, price= product.price,
        image= product.image, description=product.description, tags=tag_list_f, rating=rating,
        rpic=rpic, p_name=p_name)

        listings.append(list_obj)

    # if something gets passed into the form, redirct to the query list 
    # else display products 
    if len(products) != 20:
        return render_template('product.html', avail_listings = listings, need_next=False, page=page, ph = 'Search here...')
    return render_template('product.html', avail_listings = listings, need_next=True, page=page, ph = 'Search here...')

# Originally done using javascript, but now takes in a query_id made up of the sort query as well as the 
# search parameter (listings vs. tags). The query contents are what is typed into the search bar to be found.
@bp.route('/products/<string:query_id>/<string:query_contents>/<int:page>', methods=['GET', 'POST'])
def show_queried_product_list(query_id, query_contents, page):
    # Get the page number, set initial values for the place holder, listings, and products to their inital values
    page = int(page)
    start = int(page*20)
    ph = ''
    reviews = -1

    # Try to query the information from the sort checkbox, try and if it doesn't work set it to empty
    try:
        sort = str(request.form['sort'])
    except:
        sort = ''

    # Try to query the information from the filter checkbox, try and if it doesn't work set it to empty
    try:
        filter = str(request.form['filter'])
    except:
        filter = ''

    # Try to get the query contents, if it doesnt return anything set it equal to no_search_term and set 
    # the placeholder to search here so they can input a search
    try:
        t_query_contents = str(request.form['query'])
    except:
        t_query_contents = 'no_search_term'
        ph = "Search here..."
    if not t_query_contents:
        t_query_contents = 'no_search_term'
        ph = "Search here..."

    # If its a go button click need to use data from form, not data from previous page
    # If using data from form, should set ph equal to the query contents so the user can see what they 
    # searched for. If the query contents is empty (i.e. equal to temp), set it equal to the placeholder values.
    if query_contents == 'temp':
        query_contents = t_query_contents
    elif query_contents != 'no_search_term':
        ph = query_contents

    # If sort or filter has values, redirect and replace temps with appropriate info. If it doesn't have values
    # redirect to the generic product page. 
    # Redirect so page with temp as variable is not fully rendered, dont want user to be able to swipe back to it
    if sort or filter:
        query_id = sort+filter
        return redirect(url_for('product.show_queried_product_list', query_id=query_id, query_contents=query_contents, page = 0))
    if query_id == 'temp' and query_contents == 'no_search_term' and page == 0:
        return redirect(url_for('product.show_product_list',  page = 0))

    if query_contents == 'no_search_term':
        query_contents = ''

    listings = []
    products = []

    # For each of the query_ids perform a different query. Sort by the id given and return the listing objects
    # so they can be rendred by the final template. Options include 12 combinations, between each of the query_ids
    # and the searches. Some of the combinations can be adjusted together, i.e. sort but no query parameter could
    # technically go with either, but I paired it with the ascending sort case.
    if query_id == '' and query_contents == '':
        # Nether query_id or contents exist, redirect to generic product page
        return redirect(url_for('product.show_product_list',  page = 0))
    elif query_id == 'ln':
        products = Listing.get_all_listings_ln(start=start, query=query_contents)
        # Search by listing name 
        # for each product get the tags associated to display, as well as the rating information for the given
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'tn':
        products = Listing.get_all_listings_tn(start=start, query=query_contents)
        # Search by tag name
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 


            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'pn':
        products = Listing.get_all_listings_pn(start=start, query=query_contents)
        # Search by listing name 
        # for each product get the tags associated to display, as well as the rating information for the given
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'naln' or query_id == 'na':
        products = Listing.get_all_listings_ln_na(start=start, query=query_contents)
        # Display in name ascending order, search by listing name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'natn':
        products = Listing.get_all_listings_tn_na(start=start, query=query_contents)
        # Display in name ascending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)
            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name


            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'napn':
        products = Listing.get_all_listings_pn_na(start=start, query=query_contents)
        # Display in name ascending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'ndln' or query_id == 'nd':
        products = Listing.get_all_listings_ln_nd(start=start, query=query_contents)
        # Display in name descending order, search by listing name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:

                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)

    elif query_id == 'ndtn':
        products = Listing.get_all_listings_tn_nd(start=start, query=query_contents)
        # Display in name descending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:

                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'ndpn':
        products = Listing.get_all_listings_pn_nd(start=start, query=query_contents)
        # Display in name descending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'paln' or query_id == 'pa':
        products = Listing.get_all_listings_ln_pa(start=start, query=query_contents)
        # Display in price ascending order, search by listing name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id)

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'patn':
        products = Listing.get_all_listings_tn_pa(start=start, query=query_contents)
        # Display in price ascending order, search by tag name if search term exists

        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'papn':
        products = Listing.get_all_listings_pn_pa(start=start, query=query_contents)
        # Display in price ascending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,

            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'pdln' or query_id == 'pd':
        products = Listing.get_all_listings_ln_pd(start=start, query=query_contents)
        # Display in price descending order, search by listing name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:

                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'pdtn':
        products = Listing.get_all_listings_tn_pd(start=start, query=query_contents)
        # Display in price descending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:

                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'pdpn':
        products = Listing.get_all_listings_pn_pd(start=start, query=query_contents)
        # Display in price descending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'raln' or query_id == 'ra':
        products = Listing.get_all_listings_ln_ra(start=start, query=query_contents)
        # Display in rating ascending order, search by listing name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:

                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'ratn':
        products = Listing.get_all_listings_tn_ra(start=start, query=query_contents)
        # Display in rating ascending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'rapn':
        products = Listing.get_all_listings_pn_ra(start=start, query=query_contents)
        # Display in rating ascending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'rdln' or query_id == 'rd':
        products = Listing.get_all_listings_ln_rd(start=start, query=query_contents)
        # Display in rating descending order, search by listing name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)


            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name


            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)
    elif query_id == 'rdtn':
        products = Listing.get_all_listings_tn_rd(start=start, query=query_contents)
        # Display in rating descending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 

            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)

            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name

            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)
            listings.append(list_obj)
    elif query_id == 'rdpn':
        products = Listing.get_all_listings_pn_rd(start=start, query=query_contents)
        # Display in rating descending order, search by tag name if search term exists
        for product in products:
            rsummary = Rating.product_summary(product.product_id) 
            # If the summary does not exist, set reviews to 0 so that we display no reviews instead of the 
            # rating and the image of the stars.
            if rsummary[1] == "N/A" or rsummary[1] is None:
                rating = "N/A"
                rpic = '../static/css/images/0stars.png'
            else:
                rating = round(rsummary[1], 2)
                rpicV = int(round(rating))
                rpic = get_rpic(rpicV)


            p_info = Product.get_product_info(product.product_id)
            p_name = p_info.p_name


            l_tag_pairs = ListingsHaveTags.get_tags(product.l_id)
            tag_list = []
            for row in l_tag_pairs:
                tag_list.append(row.tag)
            if not tag_list:
                tag_list_f = ""
            else:
                tag_list_f = ", ".join(tag_list)
            list_obj = ListingWithTags(l_id=product.l_id, seller_id=product.seller_id,
            product_id=product.product_id,listing_name=product.listing_name, price= product.price,
            image= product.image, description=product.description, tags=tag_list_f, rating=rating,
            rpic=rpic, p_name=p_name)

            listings.append(list_obj)

    # filter tag table with l_ids based on query, then get all listings based on this list of l_ids
    # then turns them into listings with tags again

    # If query contents is still empty (no query_id) add no_search_term
    # Update placeholder to show query contents 
    if query_contents == '':
        query_contents = 'no_search_term'
    if ph == '':
        ph = query_contents

    # If length of the products queried is less than 20, then render with need_next is false so next
    # page is not displayed. 

    if len(products) != 20:
        return render_template('product.html', avail_listings = listings, need_next=False, qid=query_id, qc = query_contents, page=page, ph = ph)
    return render_template('product.html', avail_listings = listings, need_next=True, qid=query_id, qc = query_contents, page=page, ph = ph)




class NewTagForm(FlaskForm):
    tag_name = StringField(_l('Tag Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Create New Tag'))

# Create a new product, only if the user is authenticated and is a seller 
@bp.route('/products/new_tag', methods=['GET', 'POST'])
def create_new_tag():
    if not current_user.is_authenticated or not PublicProfile.get_if_seller(current_user.id):
        flash('You are not authenticated to add new tags!')
        return redirect(url_for('product.show_product_list', page = 0))
    form = NewTagForm()

    if form.validate_on_submit():
        if Tags.add_tag(form.tag_name.data) is not None:
            flash('Congratulations, you have created a new tag!')
        else:
            flash('Tag unable to be added!')
        # redirect back to user page so they can see where to add a new product?
        # for now we'll do generic product page
        # redirect to page to create a listing for this product?
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('product.show_product_list', page = 0)

        return redirect(next_page)
    return render_template('newTag.html', title='New Tag', form=form)

# New product form which you can use to update product name only 
class NewProductForm(FlaskForm):
    product_name = StringField(_l('Product Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Create Product'))

# Create a new product, only if the user is authenticated and is a seller 
@bp.route('/products/new_product', methods=['GET', 'POST'])
def create_new_product():
    if not current_user.is_authenticated or not PublicProfile.get_if_seller(current_user.id):
        flash('You are not authenticated to add products!')
        return redirect(url_for('product.show_product_list', page = 0))
    form = NewProductForm()

    if form.validate_on_submit():
        if (product := Product.add_new_product(form.product_name.data,
                current_user.id)):
            flash('Congratulations, you have created a new product!')
            flash('Please create a new version of the product in order for it to be displayed.')
        else:
            flash('Product could not be created.')
            redirect(url_for('product.show_product_list', page = 0))
        # redirect back to user page so they can see where to add a new product?
        # for now we'll do generic product page
        # redirect to page to create a listing for this product?
        next_page = request.args.get('next')
        product_id = product.p_id
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('inventory.create_new_listing', product_id = product_id)

        return redirect(next_page)
    return render_template('newProduct.html', title='New Product', form=form)

# Update a product, change the product name
class UpdateProductForm(FlaskForm):
    product_name = StringField(_l('New Product Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Product'))

# Update the product - first check is the user is authenticated, then if they are a seller and are the
# seller who first created this prodcut (need this in order to update)
@bp.route('/products/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    # this check might end up being redundant
    product = Product.get_products_fs(product_id)
    if not current_user.is_authenticated or current_user.id != product.first_seller_id:
        flash('You are not authenticated to edit this product!')
        return redirect(url_for('product.show_product_list', page = 0))
    form = UpdateProductForm()

    if form.validate_on_submit():
        # if valid form, they selected a product they created (use current_user.id in query)
        if Product.update_p_name(form.product_name.data, product_id):
            flash('Congratulations, you have updated the product name to ' + form.product_name.data)
        # redirect back to user page so they can see where to add a new product?
        # for now we'll do generic product page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('product.show_product_list', page = 0)

        return redirect(next_page)
    return render_template('updateProduct.html', title='Update Product', product_name=product.p_name, form=form)

# Show the listing page for a given product and listing ID, check if the user can edit the product (i.e.)
# check if they are the user that is the first creater of the prdouct to see if they can edit it.
@bp.route('/products/<int:product_id>/<int:listing_id>', methods=['GET', 'POST'])
def show_listing_page(product_id: int, listing_id: int):
    product = Product.get_products_fs(product_id)
    can_edit_product = current_user.is_authenticated and current_user.id == product.first_seller_id
    listing_info = Listing.get_listing_info(listing_id)
    can_create_listing = current_user.is_authenticated and PublicProfile.get_if_seller(current_user.id)
    can_update_listing = current_user.is_authenticated and current_user.id == listing_info.seller_id
    listings = Listing.get_listings_from_product(product_id)
    seller = User.get(listing_info.seller_id)
    inventory_quantity=Inventory.get_quantity(listing_id)
    # inventory_quantity = (Inventory.get(listing_id)).quantity
    review_count, avg_rating = Rating.product_summary(product_id)
    l_tag_pairs = ListingsHaveTags.get_tags(listing_id)
    tag_list = []
    for row in l_tag_pairs:
        tag_list.append(row.tag)
    if not tag_list:
        tag_list_f = ""
    else:
        tag_list_f = ", ".join(tag_list)
    # Round the average rating but only if its not a string
    if avg_rating != "N/A" and avg_rating is not None:
        avg_rating = round(avg_rating, 2)

    return render_template('productPage.html', listing = listing_info, seller = seller, quantity = inventory_quantity,
     product_listings=listings, product = product, count=review_count, avg=avg_rating, can_edit_product=can_edit_product,
     tag_list_f =tag_list_f, can_create_listing=can_create_listing, can_update_listing=can_update_listing)


# Route for creating additions to your cart, redirect immidiately after to the show_listing_page of the 
# id that they justgit came from. Flash a message explaining whether they added the it successfully or flasj
# them a message saying that it did not work.
@bp.route('/products/<int:product_id>/<int:listing_id>/adding_to_cart', methods=['GET', 'POST'])
def add_to_cart(product_id: int, listing_id: int):
    # l_id = Listing.get_listing_info(listing_id).l_id
    inventory_quantity = int((Inventory.get(listing_id)).quantity)
    listing_name = Listing.get_listing_info(listing_id).listing_name
    quantity = int(request.form['quantity'])
    if current_user.is_authenticated and (quantity <= inventory_quantity):
        Cart.add_to_cart(current_user.id, listing_id, quantity)
        flash('You have added ' + str(quantity) + ' ' + str(listing_name) + ' to your cart')
    else:
        flash('Unable to add ' + str(quantity) + ' ' + str(listing_name) + ' to your cart. Please ensure the following: Is user logged in? Is the product already in your cart? Is the quantity under the maximum?')

    # should we redirect to user cart here?
    return redirect(url_for('product.show_listing_page', product_id = product_id,listing_id = listing_id))

# Route for viewing all the tags that you could possibly add to your listing
@bp.route('/products/tags', methods=['GET', 'POST'])
def see_tags():
    tags = Tags.get_all_tags()
    return render_template('allTags.html', tags=tags)
