from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from flask import render_template, redirect, url_for, request, flash
from flask.ctx import copy_current_request_context
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from werkzeug.urls import url_parse
from flask_wtf.form import FlaskForm
from flask import Markup
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.core import FloatField, SelectField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import URL, DataRequired, Email, EqualTo, ValidationError
from flask import current_app as app
from app import db
from app.models.cart import Cart
from app.models.inventory import Inventory, InventoryWithName
from app.models.tags import Tags, ListingsHaveTags
from .models.seller_orders import SellerOrders #can remove this later
from .db import DB

from app.models.public_page import PublicProfile

from .models.user import User
from .models.product import Product
from .models.listing import Listing
from .models.product import Product
from .models.purchase import Purchase
from .models.rating import Rating


from flask import Blueprint
bp = Blueprint('inventory', __name__)

# show all listings belonging to logged in seller
@bp.route('/your_inventory', methods=['GET', 'POST'])
def show_inventory():
    inventory = InventoryWithName.products_from_seller(current_user.id)
    return render_template('your_inventory.html', seller_inventory=inventory)
    
# delete listings from current seller's inventory
@bp.route('/your_inventory/<int:listing_id>/delete_from_inventory', methods=['GET', 'POST'])
def delete_product_inventory(listing_id):
    Inventory.delete_product(current_user.id, listing_id) 
    #inventory = Inventory.products_from_seller(current_user.id)   
    #maybe add flash message saying deleted
    flash("Your listing has been deleted!")
    return redirect(url_for('inventory.show_inventory'))

# displays current quantity of a seller's listing
@bp.route('/quantity/<int:listing_id>', methods=['GET', 'POST'])
def quantity(listing_id):
    currQuantity = Inventory.get_quantity(listing_id)
    return render_template('quantity.html', quantity=currQuantity)

# changes the quantity of a seller's listing
@bp.route('/change_quantity_to/<int:listing_id>', methods=['GET','POST'])
def change_quantity_to(listing_id):
    if request.method == 'POST': 
        new_quantity= request.form['quantityform']
        old_quantity = Inventory.get_quantity(listing_id)
        print(Inventory.change_quantity(new_quantity, current_user.id, listing_id))
    return render_template('quantity.html', quantity=Inventory.get_quantity(listing_id))

# creates a new listing for a seller and puts it in their inventory
@bp.route('/your_inventory/<int:product_id>/new_listing', methods=['GET', 'POST'])
def create_new_listing(product_id):
    # check if authenticated/is seller
    if not current_user.is_authenticated or not PublicProfile.get_if_seller(current_user.id):
        flash('You are not authenticated to add product listings!')
        return redirect(url_for('product.show_product_list', page = 0))
    form = NewListingForm()
    p_name = Product.get_product_info(product_id).p_name
    # maybe let them add tags as well? need a form to update listing
    if form.validate_on_submit():            
        # add to inventory as well
        listing_id=Listing.add_new_listing(current_user.id,
                    product_id,
                    form.listing_name.data,
                    form.price.data,
                    form.image_url.data,
                    form.description.data).l_id 
        flash('Congratulations, you have created a new listing!')
        quantity=0
        Inventory.add_products(listing_id, quantity, current_user.id)
        flash('Your new listing was added to your inventory!')
        # redirect back to the inventory page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('inventory.show_inventory')
        return redirect(next_page)
    return render_template('newListing.html', title='New Listing', product_id=product_id, p_name=p_name, form=form)


    # creates variables and format for new listing
class NewListingForm(FlaskForm):
    listing_name = StringField(_l('Listing Name'), validators=[DataRequired()])
    price = FloatField(_l('Price'), validators=[DataRequired()])
    image_url = StringField(_l('Image URL'))
    description = StringField(_l('Listing Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Create Listing'))

# updates current seller's listing
@bp.route('/your_inventory/<int:product_id>/<int:listing_id>/update_listing', methods=['GET', 'POST'])
def update_new_listing(product_id,listing_id):
    
    listing = Listing.get_listing_info(listing_id)
    if not current_user.is_authenticated or not PublicProfile.get_if_seller(current_user.id):
        flash('You are not authenticated to edit this listing!')
        return redirect(url_for('product.show_product_list', page = 0))
    form = UpdateListingForm()
    # maybe let them add tags as well? need a form to update listing
    if form.validate_on_submit():
        if form.listing_name.data != "":
            Listing.update_l_name(form.listing_name.data, listing_id)
            flash('Congratulations, you have updated the listing name!')
        if form.price.data != 0.0:
            Listing.update_price(form.price.data, listing_id)
            flash('Congratulations, you have updated the listing price!')
        if form.image_url.data != "":
            Listing.update_image(form.image_url.data, listing_id)
            flash('Congratulations, you have updated the listing image!')
        if form.description.data != "":
            Listing.update_description(form.description.data, listing_id)
            flash('Congratulations, you have updated the listing description!')
        if form.tag.data != "":
            try:
                ListingsHaveTags.add_new_tag_to_listing(listing_id, form.tag.data)
                flash('Congratulations, you have add the tag ' + form.tag.data + ' to your listing!')
            except Exception:
                flash('This tag could not be added. Please ensure ' + form.tag.data + ' is an existing tag, or add it!')
        # redirect back to this product page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('inventory.show_inventory')
            return redirect(next_page)
    return render_template('updateListing.html', title='Update Listing', form=form, listing_name=listing.listing_name)


# class that takes care of formatting for update listing form  
class UpdateListingForm(FlaskForm):
    # t = Product.get_all_products(True)
    # product_id = SelectField(_l('Select Existing Product', choices = PRODUCT_CHOICES, validators=[DataRequired()]))
    listing_name = StringField(_l('Listing Name'))
    price = FloatField(_l('Price'), default=0.0) 
    image_url = StringField(_l('Image URL'))
    tag = StringField(_l('Existing Tag to Add'))
    # image_url = URL(_l('Image URL')), 
    description = StringField(_l('Listing Description'))
    submit = SubmitField(_l('Update Listing'))






