from datetime import date, datetime
from flask import current_app as app
from sqlalchemy import text

class SellerOrderDetails: 
    def __init__(self, l_id, seller_id, p_id, listing_name, quantity, price, user_id, fulfilled, dt):
        self.l_id = l_id
        self.s_id = seller_id
        self.p_id = p_id
        self.l_name = listing_name
        self.quantity = quantity
        self.price = price
        self.user_id = user_id
        self.fulfilled = fulfilled
        self.datetime_fulfilled = dt
        self.subtotal = 0

    # Get contents of a particular order where
    #  only order contents of logged in seller are shown
    @staticmethod 
    def get_order(order_id, seller_id):
        rows = app.db.execute("""
            SELECT DISTINCT OrderContents.l_id,
            Listing.seller_id, Listing.product_id, Listing.listing_name, OrderContents.quantity, 
            OrderContents.price, OrderContents.u_id, OrderContents.item_fulfilled, 
            OrderContents.datetime_fulfilled  
            FROM OrderContents, Listing
            WHERE (OrderContents.l_id IN (SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= :seller_id) 
            AND  OrderContents.o_id= :order_id)
            AND (Listing.l_id IN(SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= :seller_id)
            AND Listing.l_id IN(SELECT DISTINCT l_id FROM OrderContents WHERE OrderContents.o_id= :order_id)
            AND Listing.l_id = OrderContents.l_id);
            
        """, order_id = order_id, seller_id=seller_id)

        print(rows[0])
        
        return [SellerOrderDetails(*row) for row in rows]

    # marks a line item as fulfilled
    @staticmethod
    def fulfill_order(order_id, listing_id):
        try:
           
            rows = app.db.execute("""
            UPDATE OrderContents SET item_fulfilled = B'1'  WHERE l_id = :listing_id and o_id = :order_id
            """, order_id = order_id, listing_id = listing_id)
            return "Success"
        except:
            return "FAIL HAHA"

# UPDATE OrderContents SET item_fulfilled = B'1'  WHERE (l_id = 110 and o_id = 233
#             and (SELECT DISTINCT l_id FROM Listing WHERE Listing.l_id IN(SELECT DISTINCT l_id FROM Listing WHERE Listing.product_id= 10)));
# # SELECT ojl.l_id, Listing.seller_id, Listing.product_id, Product.p_name, Listing.listing_name, 
#             ojl.quantity, ojl.price, ojl.u_id, ojl.item_fulfilled, ojl.datetime_fulfilled FROM ojl, Listing, Product 
#             WHERE Listing.seller_id = :seller_id 
# def get_seller_orders(seller_id):
    #     rows = app.db.execute("""
    #         WITH oi AS (SELECT * FROM OrderContents),
    #         ojl AS 
    #             (SELECT oi.l_id, Listing.seller_id, Listing.listing_name,
    #             oi.quantity, oi.u_id, oi.item_fulfilled, oi.datetime_fulfilled
    #             FROM oi, Listing
    #             WHERE Listing.l_id = oi.l_id)
    #         SELECT ojl.l_id, Listing.seller_id, Listing.listing_name, ojl.quantity, ojl.u_id,
    #         ojl.item_fulfilled, ojl.datetime_fulfilled FROM ojl, Listing WHERE Listing.seller_id = :seller_id
    #     """, seller_id= seller_id)




# SELECT * FROM OrderContents 
# WHERE l_id IN(SELECT * FROM Listing WHERE Listing.seller_id =0) AND
# o_id = 41;

# SELECT * FROM OrderContents 
# WHERE l_id IN(SELECT l_id FROM Listing WHERE Listing.seller_id= :seller_id) AND o_id = :order_id;


# SELECT Listing.l_id, Listing.product_id, Product.p_name, Listing.listing_name FROM OrderContents, Listing, Product 
#             WHERE l_id IN(SELECT l_id FROM Listing WHERE Listing.seller_id= 0) AND o_id = 41;

# SELECT DISTINCT OrderContents.l_id,
#             OrderContents.quantity, OrderContents.price, OrderContents.u_id, OrderContents.item_fulfilled, 
#             OrderContents.datetime_fulfilled  FROM OrderContents WHERE (OrderContents.l_id IN (SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= 0) AND  OrderContents.o_id=42);
            
# SELECT DISTINCT Listing.seller_id, Listing.product_id, Listing.listing_name, Listing.l_id
#             FROM Listing 
#             WHERE l_id IN(SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= 0)
#             AND l_id IN(SELECT DISTINCT l_id FROM OrderContents WHERE OrderContents.o_id= 42);

# SELECT DISTINCT OrderContents.l_id,
#             OrderContents.quantity, OrderContents.price, OrderContents.u_id, OrderContents.item_fulfilled, 
#             OrderContents.datetime_fulfilled, Listing.seller_id, Listing.product_id, Listing.listing_name
#             FROM OrderContents, Listing
#             WHERE (OrderContents.l_id IN (SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= 0) AND  OrderContents.o_id=42)
#             AND (Listing.l_id IN(SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= 0)
#             AND Listing.l_id IN(SELECT DISTINCT l_id FROM OrderContents WHERE OrderContents.o_id= 42));




















# SELECT DISTINCT OrderContents.l_id, Listing.seller_id, Listing.product_id, Listing.listing_name, 
#             OrderContents.quantity, OrderContents.price, OrderContents.u_id, OrderContents.item_fulfilled, 
#             OrderContents.datetime_fulfilled  FROM OrderContents, Listing 
#             WHERE OrderContents.l_id IN(SELECT DISTINCT l_id FROM Listing WHERE Listing.seller_id= 0) 
#             AND o_id=42;

# SELECT DISTINCT OrderContents.l_id, Listing.seller_id, Listing.product_id, Listing.listing_name, 
#         OrderContents.quantity, OrderContents.price, OrderContents.u_id, OrderContents.item_fulfilled, 
#         OrderContents.datetime_fulfilled  FROM OrderContents, Listing 
#         WHERE (OrderContents.l_id IN() 
#         AND OrderContents.o_id=42);
