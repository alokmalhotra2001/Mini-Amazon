from flask import current_app as app

class SellerOrders: 
    def __init__(self, o_id, placed, fulfilled, num_items):
        self.o_id = o_id
        self.placed = placed
        self.fulfilled = fulfilled
        self.num_items = num_items
        
        # self.l_id = l_id
        # self.s_id = seller_id
        # self.l_name = listing_name
        # self.quantity = quantity
        # self.user_id = user_id
        # self.fulfilled = fulfilled
        # self.datetime_fulfilled = dt
        
    # def get_seller_history(seller_id):
    #     print(seller_id)
    #     rows = app.db.execute('''
    # SELECT id, placed, fulfilled, num_items
    # FROM Orders
    # WHERE seller_id = :seller_id
    # ''', seller_id=seller_id)
    # #make sure to revert id back to buyer_id
    #     print([SellerOrders(*row) for row in rows])
    #     print(SellerOrders(*(rows[0])))
    #     return [SellerPrders(*row) for row in rows]

    # Get an entire user's current cart
    # select all order contents, get orders with same order id and display all of these orders for that specific seller
    
    @staticmethod
    def get_seller_orders(seller_id):
        rows = app.db.execute("""
            SELECT DISTINCT id, placed, fulfilled, num_items  FROM Orders WHERE id IN(SELECT DISTINCT o_id FROM OrderContents WHERE l_id IN(
            SELECT DISTINCT l_id FROM Listing WHERE seller_id = :seller_id))
            ORDER BY placed DESC;
        """, seller_id= seller_id)
        return [SellerOrders(*row) for row in rows]

    def get_all_seller_orders_asc(seller_id):
        rows = app.db.execute("""
            SELECT DISTINCT id, placed, fulfilled, num_items  FROM Orders WHERE id IN(SELECT DISTINCT o_id FROM OrderContents WHERE l_id IN(
            SELECT DISTINCT l_id FROM Listing WHERE seller_id = :seller_id))
            ORDER BY placed ASC;
        """, seller_id= seller_id)
        return [SellerOrders(*row) for row in rows]

    def get_orders_fulfilled(seller_id):
        rows = app.db.execute("""
            SELECT DISTINCT id, placed, fulfilled, num_items  FROM Orders WHERE id IN(SELECT DISTINCT o_id FROM OrderContents WHERE l_id IN(
            SELECT DISTINCT l_id FROM Listing WHERE seller_id = :seller_id)) AND fulfilled = B'1'
            ORDER BY placed DESC;
        """, seller_id=seller_id)
        return [SellerOrders(*row) for row in rows]

    def get_orders_unfulfilled(seller_id):
        rows = app.db.execute("""
            SELECT DISTINCT id, placed, fulfilled, num_items  FROM Orders WHERE id IN(SELECT DISTINCT o_id FROM OrderContents WHERE l_id IN(
            SELECT DISTINCT l_id FROM Listing WHERE seller_id = :seller_id)) AND fulfilled = B'0'
            ORDER BY placed DESC;
        """, seller_id=seller_id)
        return [SellerOrders(*row) for row in rows]

    @staticmethod
    def fulfill_whole_order(order_id):
        print(f"IMM OVR HERE {order_id}")
        try:
            rows = app.db.execute("""
            UPDATE Orders SET fulfilled = B'1' WHERE id = :order_id;
            """, order_id = order_id)
            return 'Successs'
        except:
            return 'Fail'



    # @staticmethod
    # def get_seller_orders(seller_id):
    #     rows = app.db.execute("""
    #         WITH oi AS (SELECT * FROM OrderContents),
    #         ojl AS 
    #             (SELECT oi.o_id, oi.l_id, Listing.seller_id, Listing.listing_name,
    #             oi.quantity, oi.u_id, oi.item_fulfilled, oi.datetime_fulfilled
    #             FROM oi, Listing
    #             WHERE Listing.l_id = oi.l_id),
    #         ocs AS
    #             (SELECT ojl.o_id, ojl.l_id, Listing.seller_id, Listing.listing_name, ojl.quantity, ojl.u_id,
    #             ojl.item_fulfilled, ojl.datetime_fulfilled FROM ojl, Listing WHERE Listing.seller_id = :seller_id)
    #         SELECT Orders.id, Orders.placed,Orders.fulfilled, Orders.num_items FROM ocs, Orders
    #         WHERE ocs.o_id= Orders.id;
        
    #     """, seller_id= seller_id)

    #     #print(rows[0])
    #     return [SellerOrders(*row) for row in rows]

    # SELECT DISTINCT * FROM Orders WHERE id IN(SELECT DISTINCT o_id FROM OrderContents WHERE l_id IN(
    #     SELECT DISTINCT l_id FROM Listing WHERE seller_id =0));


    # #old order contents
    # @staticmethod 
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

    #     print(rows[0])

        
    #     return [SellerOrders(*row) for row in rows]

    #     WITH oi AS (SELECT * FROM OrderContents),
    #         ojl AS 
    #             (SELECT oi.o_id, oi.l_id, Listing.seller_id, Listing.listing_name,
    #             oi.quantity, oi.u_id, oi.item_fulfilled, oi.datetime_fulfilled
    #             FROM oi, Listing
    #             WHERE Listing.l_id = oi.l_id),
    #         ocs AS(SELECT ojl.o_id, ojl.l_id, Listing.seller_id, Listing.listing_name, ojl.quantity, ojl.u_id,
    #         ojl.item_fulfilled, ojl.datetime_fulfilled FROM ojl, Listing WHERE Listing.seller_id = :seller_id)
    #         SELECT ocs.o_id, Orders.id, Orders.placed,Orders.fulfilled, Orders.num_items FROM ocs, Orders
    #         WHERE ocs.o_id= Orders.id;
            
         
         
         
         
         
         
         
    #      WITH oi AS (SELECT * FROM OrderContents),
    #         ojl AS 
    #             (SELECT oi.l_id, Listing.seller_id, Listing.listing_name,
    #             oi.quantity, oi.u_id, oi.item_fulfilled, oi.datetime_fulfilled
    #             FROM oi, Listing
    #             WHERE Listing.l_id = oi.l_id)
