from flask import render_template
from flask_login import current_user
import datetime
from flask import jsonify

from app.models.public_page import PublicProfile
from .models.public_page import PublicProfile

from .models.product import Product
from .models.listing import Listing
from .models.purchase import Purchase

from .models.inventory import Inventory
from .models.rating import Rating
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    # turn into some form of better display page?
    
    # get all available products for sale:
    # products = Listing.get_all_listings(True)
    # find the products current user has bought:

    #if current_user.is_authenticated:
        #purchases = Purchase.get_all_by_uid_since(
            #current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #else:
    # if current_user.is_authenticated:
    #     seller = PublicProfile.get_if_seller(current_user.id)
    purchases = []
    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        cart_items = Cart.get_cart(current_user.id)
    else:
        cart_items = []
        seller= False

    return render_template('index.html', purchase_history=purchases, mycart=cart_items)

    #return jsonify(products)
