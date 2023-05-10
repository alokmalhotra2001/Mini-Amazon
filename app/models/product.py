from flask import current_app as app

class Product:
    def __init__(self, p_id, p_name, first_seller_id):
        self.p_id = p_id
        self.p_name = p_name
        self.first_seller_id = first_seller_id

    # Get the product info for a product given a product id
    @staticmethod
    def get_product_info(p_id):
        rows = app.db.execute('''
SELECT p_id, p_name, first_seller_id
FROM Product
WHERE p_id = :p_id
''',
                              p_id=p_id)
        return Product(*(rows[0]))

    # Get all the products and their information 
    @staticmethod
    def get_all_products(available=True):
        rows = app.db.execute('''
SELECT p_id, p_name, first_seller_id
FROM Product
''',
                            available=available)
        return [Product(*row) for row in rows]

    # Get all the products given a seller id
    @staticmethod
    def get_all_products_with_fs(first_seller, available=True):
        rows = app.db.execute('''
SELECT p_id, p_name, first_seller_id
FROM Product
WHERE first_seller_id = :first_seller
''',
                            first_seller=first_seller, available=available)
        return [Product(*row) for row in rows]

    # Get all products given, same as product_info but kept for dependencies sake
    @staticmethod
    def get_products_fs(p_id, available=True):
        rows = app.db.execute('''
SELECT p_id, p_name, first_seller_id
FROM Product
WHERE p_id = :p_id
''',
                            p_id=p_id, available=available)
        return Product(*(rows[0]))

    # Adds a new product given the necessary info
    @staticmethod
    def add_new_product(p_name, first_seller_id):
        try:
            rows = app.db.execute('''
    INSERT INTO Product (p_name, first_seller_id) 
    VALUES (:p_name, :first_seller_id)
    RETURNING p_id
    ''',
                                p_name = p_name, first_seller_id = first_seller_id)
            id = rows[0][0]
            return Product.get_product_info(id)
        except Exception:
            # Issue with creating listing
            return None
            
    # Updates the product name 
    @staticmethod
    def update_p_name(new_p_name, p_id):
        try:
            rows = app.db.execute('''
        UPDATE Product SET p_name = :new_p_name 
        WHERE p_id = :p_id
        RETURNING *
        ''', p_id=p_id, new_p_name=new_p_name)
            if rows is not None:
                return Product(*(rows[0]))
        except Exception:
            return None