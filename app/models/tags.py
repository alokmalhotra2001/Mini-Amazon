from flask import current_app as app

class ListingsHaveTags:
    def __init__(self, l_id, tag):
        self.l_id = l_id
        self.tag = tag

    @staticmethod
    def get_tags(l_id):
        rows = app.db.execute('''
    SELECT l_id, tag_name
    FROM ListingsHaveTags
    WHERE l_id = :l_id
    ''',
                                l_id=l_id)
        return [ListingsHaveTags(*row) for row in rows]

        # Adds a new tag to an existing product
    @staticmethod
    def add_new_tag_to_listing(l_id, tag_name):
        try:
            rows = app.db.execute('''
    INSERT INTO ListingsHaveTags (l_id, tag_name)
    VALUES (:l_id, :tag_name)
    ''',
                                l_id=l_id, tag_name=tag_name)
            return 1
        except Exception:
            return 0

         # Delete a tag from an existing product
    @staticmethod
    def delete_tag_from_listing(l_id, tag_name):
        try:
            rows = app.db.execute('''
    DELETE FROM ListingsHaveTags 
    WHERE l_id = :l_id AND reviewee = :reviewee
    ''',
                                l_id=l_id, tag_name=tag_name)
            return 1
        except Exception:
            return 0

class Tags:
    def __init__(self, tag):
        self.tag = tag

    @staticmethod
    def get_all_tags():
        try:
            rows = app.db.execute('''
    SELECT * FROM Tags
    ''')
            return [Tags(*row) for row in rows]
        except Exception:
            return None

    @staticmethod
    def add_tag(tag_name):
        try:
            rows = app.db.execute('''
    INSERT INTO Tags (name)
    VALUES (:tag_name)
    RETURNING * 
    ''',
                                tag_name=tag_name)
            if rows is not None:
                return Tags(*(rows[0]))
        except Exception:
            return None


class ListingWithTags:
    def __init__(self, l_id, seller_id, product_id, p_name, listing_name, price, image, description, tags, rating, rpic):

        self.l_id = l_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.listing_name = listing_name
        self.price = price
        self.image = image
        self.description = description
        self.tags = tags
        self.rating = rating
        self.rpic = rpic
        self.p_name = p_name

