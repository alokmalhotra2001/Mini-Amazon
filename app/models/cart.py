from datetime import date, datetime
from flask import current_app as app
from sqlalchemy import text

class Cart: 
    def __init__(self, l_id, l_name, image, description, p_id, product_name, seller_id, inventory, 
                quantity, price, status, user_id, balance):
        self.l_id = l_id
        self.l_name = l_name
        self.image = image
        self.description = description
        self.p_id = p_id
        self.p_name = product_name
        self.s_id = seller_id
        self.inventory = inventory
        self.quantity = quantity
        self.price = price
        self.status = status # Can manipulate this later
        self.user_id = user_id
        self.balance = balance
        self.subtotal = 0

    # Get an entire user's current cart
    @staticmethod 
    def get_cart(user_id):
        rows = app.db.execute("""
            WITH c_i AS (SELECT * FROM VersionInCart WHERE user_id = :user_id),
            c AS
                (SELECT c_i.l_id, Listing.seller_id, Listing.product_id, c_i.status, 
                c_i.quantity, Listing.price, c_i.user_id, Listing.listing_name, Listing.image, Listing.description
                FROM c_i INNER JOIN Listing
                ON Listing.l_id = c_i.l_id),
            c_j AS 
                (SELECT c.l_id, c.listing_name, c.image, c.description, c.product_id, Product.p_name AS product_name, 
                c.seller_id, c.quantity, c.price, c.status, c.user_id
                FROM c INNER JOIN Product
                ON c.product_id = Product.p_id),
            c_ji AS
                (SELECT c_j.l_id, c_j.listing_name, c_j.image, c_j.description, c_j.product_id, c_j.product_name, 
                c_j.seller_id, Inventory.quantity AS inventory, c_j.quantity, c_j.price, c_j.status, c_j.user_id
                FROM c_j INNER JOIN Inventory
                ON Inventory.id = c_j.l_id),
            cji_ub AS 
                (SELECT c_ji.l_id, c_ji.listing_name, c_ji.image, c_ji.description, c_ji.product_id, c_ji.product_name, 
                c_ji.seller_id, c_ji.inventory, c_ji.quantity, c_ji.price, c_ji.status, c_ji.user_id, Users.balance
                FROM c_ji INNER JOIN Users
                ON c_ji.user_id = Users.id) 
            SELECT * FROM cji_ub
        """, user_id = user_id)

        # print(rows)

        return [Cart(*row) for row in rows]
    
    @staticmethod # Edit quantity of particular item in cart
    def update_item_quantity(user_id, l_id, quantity):
        try:
            app.db.execute('''
            UPDATE VersionInCart SET quantity = :quantity WHERE user_id = :user_id AND l_id = :l_id
            ''', user_id = user_id, l_id = l_id, quantity = quantity)
            return 1
        except Exception:
            return -1

    @staticmethod # Remove item completely from cart
    def remove_item(user_id, l_id):
        try:
            app.db.execute('''
            DELETE FROM VersionInCart WHERE user_id = :user_id AND l_id = :l_id
            ''', user_id = user_id, l_id = l_id)
            return 1
        except Exception:
            return -1

    @staticmethod # Empty entire cart
    def empty_cart(user_id):
        try:
            app.db.execute('''
            DELETE FROM VersionInCart WHERE user_id = :user_id
            ''', user_id = user_id)
            return 1
        except Exception:
            return -1

    @staticmethod # Place order 
    def place_order(user_id):
        with app.db.engine.connect() as conn:
            # Step 1: Acquire all cart items, inventories, and user balance
            rows = conn.execute(text("""
            WITH c_i AS (SELECT * FROM VersionInCart WHERE user_id = :user_id AND status = '1'),
            c AS
                (SELECT c_i.l_id, Listing.seller_id, Listing.product_id, c_i.status, 
                c_i.quantity, Listing.price, c_i.user_id, Listing.listing_name, Listing.image, Listing.description
                FROM c_i INNER JOIN Listing
                ON Listing.l_id = c_i.l_id),
            c_j AS 
                (SELECT c.l_id, c.listing_name, c.image, c.description, c.product_id, Product.p_name AS product_name, 
                c.seller_id, c.quantity, c.price, c.status, c.user_id
                FROM c INNER JOIN Product
                ON c.product_id = Product.p_id),
            c_ji AS
                (SELECT c_j.l_id, c_j.listing_name, c_j.image, c_j.description, c_j.product_id, c_j.product_name, 
                c_j.seller_id, Inventory.quantity AS inventory, c_j.quantity, c_j.price, c_j.status, c_j.user_id
                FROM c_j INNER JOIN Inventory
                ON Inventory.id = c_j.l_id),
            cji_ub AS 
                (SELECT c_ji.l_id, c_ji.listing_name, c_ji.image, c_ji.description, c_ji.product_id, c_ji.product_name, 
                c_ji.seller_id, c_ji.inventory, c_ji.quantity, c_ji.price, c_ji.status, c_ji.user_id, Users.balance
                FROM c_ji INNER JOIN Users
                ON c_ji.user_id = Users.id) 
            SELECT * FROM cji_ub
            """), user_id = user_id)

            cart_items = [Cart(*row) for row in rows]
            
            # Step 2: Balance validation
            cart_total_price = 0
            num_cart_items = 0

            for item in cart_items:
                num_cart_items += item.quantity
                item_price_float = round(item.price, 2)
                item.price = item_price_float
                item_subtotal_float = round(item.quantity * item_price_float, 2)
                item.subtotal = item_subtotal_float
                cart_total_price += item_subtotal_float

            cart_total_price = round(cart_total_price, 2)
            user_balance = cart_items[0].balance

            if (cart_total_price > user_balance):
                delta_money = round(cart_total_price - user_balance, 2)
                delta_money2 = "{:.2f}".format(delta_money)
                return "ERROR (INSUFFICIENT FUNDS): Please add at least $" + str(delta_money) + " to your account in order to complete this purchase."

            # Step 3: Inventory validation
            for item in cart_items:
                if (item.quantity > item.inventory):
                    return "ERROR (QUANTITY INVALID): Check all quantities of cart items before submitting order again."

            # Step 4: Decrement user balance
            new_user_balance = user_balance - cart_total_price
            conn.execute(text('''
                UPDATE Users SET balance = :new_user_balance WHERE id = :user_id
            '''), user_id = user_id, new_user_balance = new_user_balance) 

            # Step 5/6: Decrement item inventories and increment seller balance for each item
            for item in cart_items:
                new_inventory = item.inventory - item.quantity
                delta_balance_seller = item.subtotal
                seller_id = item.s_id
                item_id = item.l_id
                
                conn.execute(text('''
                    UPDATE Inventory SET quantity = :new_inventory WHERE id = :item_id
                '''), new_inventory = new_inventory, item_id = item_id)
                
                conn.execute(text('''
                    UPDATE Users SET balance = balance + :delta_balance_seller WHERE id = :seller_id
                '''), delta_balance_seller = delta_balance_seller, seller_id = seller_id)


            # Step 7: Create order in orders table
            curr_dt = datetime.now()
            num_items = num_cart_items
            buyer_id = cart_items[0].user_id
            
            id = conn.execute(text('''
                INSERT INTO Orders(buyer_id, placed, fulfilled, num_items) VALUES(:buyer_id, :curr_dt, B'0', :num_items) RETURNING id
            '''), buyer_id = buyer_id, curr_dt = curr_dt, num_items = num_items).first()[0]

            # Step 8: 
            order_id = id#[0]
            print(order_id)
            
            for item in cart_items:
                item_price = item.price
                item_quant = item.quantity
                item_lid = item.l_id
                conn.execute(text('''
                    INSERT INTO OrderContents(o_id, u_id, l_id, price, quantity, item_fulfilled, datetime_fulfilled)
                    VALUES (:order_id, :buyer_id, :item_lid, :item_price, :item_quant, B'0', :curr_dt)
                '''), order_id = order_id, buyer_id = buyer_id, item_lid = item_lid, item_price = item_price, item_quant = item_quant,
                curr_dt = curr_dt)

            # Step 9: Empty cart
            conn.execute(text('''
                DELETE FROM VersionInCart WHERE user_id = :user_id AND status = '1'
            '''), user_id = user_id)
        
        return 'Success'

    @staticmethod # Move from cart item to saved for later
    def move_to_sfl(user_id, l_id):
        try:
            app.db.execute('''
            UPDATE VersionInCart SET status = B'0' WHERE user_id = :user_id AND l_id = :l_id
            ''', user_id = user_id, l_id = l_id)
            return 1
        except Exception:
            return -1

    @staticmethod # Move from saved for later to cart
    def move_to_cart(user_id, l_id):
        try:
            app.db.execute('''
            UPDATE VersionInCart SET status = B'1' WHERE user_id = :user_id AND l_id = :l_id
            ''', user_id = user_id, l_id = l_id)
            return 1
        except Exception:
            return -1
    @staticmethod
    def add_to_cart(user_id, l_id, quantity):
        try:
            rows = app.db.execute('''
    INSERT INTO VersionInCart (l_id, quantity, status, user_id) 
    VALUES (:l_id, :quantity, CAST(1 AS BIT), :user_id)
    RETURNING * 
    ''',
                                user_id = user_id, l_id=l_id, quantity = quantity)
            return 1
        except Exception:
            return 0
