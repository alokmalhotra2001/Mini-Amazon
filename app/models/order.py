from datetime import date, datetime
from flask import current_app as app
from sqlalchemy import text

class Order: 
    def __init__(self, l_id, seller_id, p_id, product_name, listing_name, quantity, price, user_id, fulfilled, dt, image):
        self.l_id = l_id
        self.s_id = seller_id
        self.p_id = p_id
        self.p_name = product_name
        self.l_name = listing_name
        self.quantity = quantity
        self.price = price
        self.user_id = user_id
        self.fulfilled = fulfilled
        self.datetime_fulfilled = dt
        self.image = image
        self.subtotal = 0

    # Get an entire user's current cart
    @staticmethod 
    def get_order(order_id):
        rows = app.db.execute("""
            WITH oi AS (SELECT * FROM OrderContents WHERE o_id = :order_id),
            ojl AS 
                (SELECT oi.l_id, Listing.seller_id, Listing.product_id, Product.p_name, Listing.listing_name,
                oi.quantity, oi.price, oi.u_id, oi.item_fulfilled, oi.datetime_fulfilled, Listing.image
                FROM oi, Listing, Product
                WHERE Listing.l_id = oi.l_id AND Listing.product_id = Product.p_id)
            SELECT * FROM ojl
        """, order_id = order_id)

        print(rows)
        
        return [Order(*row) for row in rows]

# ojl AS 
#                 (SELECT oi.l_id, Listing.seller_id, Listing.product_id, Listing.product_name, Listing.listing_name,
#                 oi.quantity, oi.price, oi.u_id, oi.item_fulfilled, oi.datetime_fulfilled
#                 FROM oi INNER JOIN Listing 
#                 ON Listing.l_id = oi.l_id)