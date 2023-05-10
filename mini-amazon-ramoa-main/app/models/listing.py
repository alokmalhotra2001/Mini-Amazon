from flask import current_app as app

class Listing:
    def __init__(self, l_id, seller_id, product_id, listing_name, price, image, description):
        self.l_id = l_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.listing_name = listing_name
        self.price = price
        self.image = image
        self.description = description

    # Get all the listing info for a given Listing ID
    @staticmethod
    def get_listing_info(l_id):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id,listing_name, price, image, description
FROM Listing
WHERE l_id = :l_id
''',
                              l_id=l_id)
        return Listing(*(rows[0])) if rows is not None else None

    # Set of pagination queries for filter based off of listing name
    @staticmethod
    def get_all_listings_ln(start, query, available=True):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id, listing_name, price, image, description
FROM Listing
WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Get searches by listing names and sort by name ascending 
    @staticmethod
    def get_all_listings_ln_na(start, query, available=True):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id, listing_name, price, image, description
FROM Listing
WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')
ORDER BY listing_name ASC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by listing names and sort by name descending 
    @staticmethod
    def get_all_listings_ln_nd(start, query, available=True):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id, listing_name, price, image, description
FROM Listing
WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')
ORDER BY listing_name DESC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by listings and sort by price ascending
    @staticmethod
    def get_all_listings_ln_pa(start, query, available=True):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id, listing_name, price, image, description
FROM Listing
WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')
ORDER BY price ASC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by listings and sort by price descending
    @staticmethod
    def get_all_listings_ln_pd(start, query, available=True):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id, listing_name, price, image, description
FROM Listing
WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')
ORDER BY price DESC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by listings and sort by ratings ascending
    @staticmethod
    def get_all_listings_ln_ra(start, query, available=True):
        rows = app.db.execute('''
WITH listings AS (SELECT l_id, seller_id, product_id, listing_name, price, image, description FROM Listing WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')),
ratings AS (SELECT reviewee AS p_id, AVG(rating) AS rating FROM productRatings GROUP BY reviewee)
SELECT listings.l_id, listings.seller_id, listings.product_id, listings.listing_name, listings.price, listings.image, listings.description FROM listings 
LEFT JOIN ratings
ON listings.product_id = ratings.p_id
ORDER BY rating ASC NULLS LAST
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by listings and sort by ratings descending
    @staticmethod
    def get_all_listings_ln_rd(start, query, available=True):
        rows = app.db.execute('''
WITH listings AS (SELECT l_id, seller_id, product_id, listing_name, price, image, description FROM Listing WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')),
ratings AS (SELECT reviewee AS p_id, AVG(rating) AS rating FROM productRatings GROUP BY reviewee)
SELECT listings.l_id, listings.seller_id, listings.product_id, listings.listing_name, listings.price, listings.image, listings.description FROM listings 
LEFT JOIN ratings
ON listings.product_id = ratings.p_id
ORDER BY rating DESC NULLS LAST
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # set of pagination queries for filtering based off of tags
    @staticmethod
    def get_all_listings_tn(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.l_id = allListings.l_id
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search by tags and sort by names ascending 
    @staticmethod
    def get_all_listings_tn_na(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.l_id = allListings.l_id
ORDER BY listing_name ASC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by tags and sort by names descending 
    @staticmethod
    def get_all_listings_tn_nd(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.l_id = allListings.l_id
ORDER BY listing_name DESC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by tags and sort by price ascending 
    @staticmethod
    def get_all_listings_tn_pa(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.l_id = allListings.l_id
ORDER BY price ASC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by tags and sort by price descending 
    @staticmethod
    def get_all_listings_tn_pd(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.l_id = allListings.l_id
ORDER BY price DESC
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by tags and sort by rating ascending 
    @staticmethod
    def get_all_listings_tn_ra(start, query, available=True):
        rows = app.db.execute('''
WITH tagged_l_ids AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing),
ratings AS (SELECT reviewee AS p_id, AVG(rating) AS rating FROM productRatings GROUP BY reviewee),
taggedListings AS (SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description
FROM tagged_l_ids INNER JOIN allListings ON tagged_l_ids.l_id = allListings.l_id)
SELECT taggedListings.l_id, taggedListings.seller_id, taggedListings.product_id, taggedListings.listing_name, taggedListings.price, taggedListings.image, taggedListings.description FROM taggedListings 
LEFT JOIN ratings
ON taggedListings.product_id = ratings.p_id
ORDER BY rating ASC NULLS LAST
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]

    # Search by tags and sort by rating descending  
    @staticmethod
    def get_all_listings_tn_rd(start, query, available=True):
        rows = app.db.execute('''
WITH tagged_l_ids AS (SELECT DISTINCT l_id FROM ListingsHaveTags WHERE LOWER(tag_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing),
ratings AS (SELECT reviewee AS p_id, AVG(rating) AS rating FROM productRatings GROUP BY reviewee),
taggedListings AS (SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description
FROM tagged_l_ids INNER JOIN allListings ON tagged_l_ids.l_id = allListings.l_id)
SELECT taggedListings.l_id, taggedListings.seller_id, taggedListings.product_id, taggedListings.listing_name, taggedListings.price, taggedListings.image, taggedListings.description FROM taggedListings 
LEFT JOIN ratings
ON taggedListings.product_id = ratings.p_id
ORDER BY rating DESC NULLS LAST
LIMIT 20
OFFSET :start
''',
                              available=available, query=query, start=start)
        return [Listing(*row) for row in rows]


    # Get all listings based on product name
    @staticmethod
    def get_all_listings_pn(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.p_id = allListings.product_id
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search product names and sort product name ascending
    @staticmethod
    def get_all_listings_pn_na(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.p_id = allListings.product_id
ORDER BY listing_name ASC
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search product names and sort product name descending
    @staticmethod
    def get_all_listings_pn_nd(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.p_id = allListings.product_id
ORDER BY listing_name DESC
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search product names and sort price ascending
    @staticmethod
    def get_all_listings_pn_pa(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.p_id = allListings.product_id
ORDER BY price ASC
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search product names and sort price descending
    @staticmethod
    def get_all_listings_pn_pd(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing)
SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings 
ON filteredListings.p_id = allListings.product_id
ORDER BY price DESC
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search product names and sort rating ascending
    @staticmethod
    def get_all_listings_pn_ra(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing),
ratings AS (SELECT reviewee AS p_id, AVG(rating) AS rating FROM productRatings GROUP BY reviewee),
listings AS (SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings ON filteredListings.p_id = allListings.product_id)
SELECT listings.l_id, listings.seller_id, listings.product_id, listings.listing_name, listings.price, listings.image, listings.description FROM listings 
LEFT JOIN ratings
ON listings.product_id = ratings.p_id
ORDER BY rating ASC NULLS LAST
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]

    # Search product names and sort rating descending
    @staticmethod
    def get_all_listings_pn_rd(start, query, available=True):
        rows = app.db.execute('''
WITH filteredListings AS (SELECT p_id FROM Product WHERE LOWER(p_name) LIKE LOWER('%' || :query || '%')),
allListings AS (SELECT * FROM Listing),
ratings AS (SELECT reviewee AS p_id, AVG(rating) AS rating FROM productRatings GROUP BY reviewee),
listings AS (SELECT allListings.l_id, allListings.seller_id, allListings.product_id, allListings.listing_name, allListings.price, allListings.image, allListings.description FROM filteredListings 
INNER JOIN allListings ON filteredListings.p_id = allListings.product_id)
SELECT listings.l_id, listings.seller_id, listings.product_id, listings.listing_name, listings.price, listings.image, listings.description FROM listings 
LEFT JOIN ratings
ON listings.product_id = ratings.p_id
ORDER BY rating DESC NULLS LAST
LIMIT 20
OFFSET :start
''',
                              available=available, start=start, query=query)
        return [Listing(*row) for row in rows]


    # Filter by listings names, no sort 
    @staticmethod
    def filter_listings(query, available=True):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id, listing_name, price, image, description
FROM Listing
WHERE LOWER(listing_name) LIKE LOWER('%' || :query || '%')
''',
                              available=available, query = query)
        return [Listing(*row) for row in rows]

    # Add a new listing given necessary inputs 
    @staticmethod
    def add_new_listing(seller_id, product_id, listing_name, price, image, description):
        print(f'{seller_id}, {product_id}, {listing_name}, {price},{image},{description}')
        try:
            rows = app.db.execute('''
    INSERT INTO Listing (seller_id, product_id, listing_name, price, image, description) 
    VALUES (:seller_id, :product_id, :listing_name, :price, :image, :description)
    RETURNING *
    ''',
                                seller_id = seller_id, product_id = product_id,
                                listing_name = listing_name, price = price, image = image,
                                description = description)
            if rows is not None:
                print(Listing(*(rows[0])))
                return Listing(*(rows[0]))
        except Exception:
            print('listing table didnt add')
            # Issue with creating listing
            return None
# INSERT INTO Listing (seller_id, product_id, listing_name, price, image, description) 
#     VALUES ( 0, 5, 'test', 3.40, 'pizzaimage.com', 'bruh idk')
#     RETURNING *;
    # Delete a listing given the listing id
    @staticmethod
    def delete_listing(l_id):
        try:
            rows = app.db.execute('''
    DELETE FROM Listing
    WHERE l_id =:l_id
    RETURNING *
    ''',
                                l_id = l_id)
            if rows is not None:
                return Listing(*(rows[0]))
        except Exception:
            return None

    # Update the listing name given a new name and listing id
    @staticmethod
    def update_l_name(new_l_name, l_id):
        try:
            rows = app.db.execute('''
        UPDATE Listing SET listing_name = :new_l_name 
        WHERE l_id = :l_id
        RETURNING *
        ''', l_id=l_id, new_l_name=new_l_name)
            if rows is not None:
                return Listing(*(rows[0]))
        except Exception:
            return None

    # Update the listing name given a new price and listing id
    @staticmethod
    def update_price(new_price, l_id):
        try:
            rows = app.db.execute('''
        UPDATE Listing SET price = :new_price 
        WHERE l_id = :l_id
        RETURNING *
        ''', l_id=l_id, new_price=new_price)
            if rows is not None:
                return Listing(*(rows[0]))
        except Exception:
            return None

    # Update the listing image given a new image url and listing id
    @staticmethod
    def update_image(new_image, l_id):
        try:
            rows = app.db.execute('''
        UPDATE Listing SET image = :new_image 
        WHERE l_id = :l_id
        RETURNING *
        ''', l_id=l_id, new_image=new_image)
            if rows is not None:
                return Listing(*(rows[0]))
        except Exception:
            return None

    # Update the listing description given a new description url and listing id
    @staticmethod
    def update_description(new_description, l_id):
        try:
            rows = app.db.execute('''
        UPDATE Listing SET description = :new_description 
        WHERE l_id = :l_id
        RETURNING *
        ''', l_id=l_id, new_description=new_description)
            if rows is not None:
                return Listing(*(rows[0]))
        except Exception:
            return None

    @staticmethod
    def get_listings_from_product(p_id):
        rows = app.db.execute('''
SELECT l_id, seller_id, product_id,listing_name, price, image, description
FROM Listing
WHERE product_id = :product_id
''',
                              product_id=p_id)
        return [Listing(*row) for row in rows]
