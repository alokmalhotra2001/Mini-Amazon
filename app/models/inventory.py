from flask import current_app as app
import sqlalchemy

class Inventory:
    def __init__(self, id, seller_id, quantity):
        self.id = id
        self.seller_id = seller_id
        self.quantity = quantity
        #add link to product page?

    @staticmethod 
    # seller can add products to their inventory
    def add_products(id, quantity, seller_id):
        try:
            app.db.execute('''
        INSERT INTO Inventory (id, seller_id, quantity) 
        VALUES (:id, :seller_id, :quantity)
        RETURNING *
        ''', id=id, quantity=quantity, seller_id=seller_id)
            return 'Success' 
        except Exception:
            return 'FAIL'

    @staticmethod 
    #seller can change quantity of a product
    def change_quantity(new_quantity, seller_id, id):
        try:
            app.db.execute('''
        UPDATE Inventory SET quantity = :new_quantity 
        WHERE seller_id = :seller_id AND id = :id
        RETURNING * 
        ''', new_quantity=new_quantity, seller_id=seller_id, id=id)
            return 'Success'
        except Exception:
            return 'FAIL'

    
    @staticmethod 
    #seller can delete products from their inventory
    def delete_product(seller_id, id):
        try:
         app.db.execute('''
        DELETE FROM Inventory
        WHERE seller_id = :seller_id AND id = :id
        ''', seller_id=seller_id, id=id)
         return 'Success'
        except Exception: 
            return 'FAIL'
    
    @staticmethod
    # gets all information of a seller
    def get(id):
        rows = app.db.execute('''
    SELECT id, seller_id, quantity
    FROM Inventory
    WHERE id = :id
    ''',
                              id=id)
        return Inventory(*(rows[0])) if rows is not None else None

    @staticmethod
    # gets all information of a seller
    def get_quantity(id):
        rows = app.db.execute('''
    SELECT id, seller_id, quantity
    FROM Inventory
    WHERE id = :id
    ''',
                              id=id)
        return Inventory(*(rows[0])) if rows is not None else None

    # gets listing id and quantity for every listing in inventory
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, quantity
FROM Inventory
''',
                              available=available)
        return [Inventory(*row) for row in rows]

class InventoryWithName:
    def __init__(self, id, seller_id, quantity, l_name):
        self.id = id
        self.seller_id = seller_id
        self.quantity = quantity
        self.l_name = l_name

       
    @staticmethod 
    #Get all products that a specific seller is offering
    #WHERE seller_id = :seller_id
    #, seller_id=seller_id)
    def products_from_seller(seller_id):
        # print(seller_id)
        try:
            rows = app.db.execute('''
            WITH inventory AS (SELECT * FROM Inventory WHERE seller_id = :seller_id),
            listingNames AS (SELECT l_id, listing_name FROM Listing)
            SELECT inventory.id, inventory.seller_id, inventory.quantity, listingNames.listing_name FROM inventory
            INNER JOIN listingNames
            ON listingNames.l_id = inventory.id
            ''', seller_id=seller_id)
            return [InventoryWithName(*row) for row in rows]
            #return [Inventory(*row) for row in rows if rows is not None else None]  
        
        except:
            print("There are no products in your inventory.")
            #return 

