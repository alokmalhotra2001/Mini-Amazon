from flask import current_app as app

class Rating:
    def __init__(self, reviewer, reviewee, rating, review, dateAndTime, helpful):
        self.reviewer = reviewer
        self.reviewee = reviewee
        self.rating = rating
        self.review = review
        self.dateAndTime = dateAndTime
        self.helpful = helpful

    @staticmethod #Get all ratings a user has written from given table
    def p_ratings_from_user(reviewer, start):
        rows = app.db.execute('''
        WITH Helpful(reviewer, reviewee, score) AS (SELECT reviewer, reviewee, sum(action) FROM productRatingsReactions GROUP BY reviewer, reviewee)

        SELECT productRatings.reviewer, productRatings.reviewee, productRatings.rating, productRatings.review, productRatings.dateAndTime, Helpful.score
        FROM productRatings LEFT OUTER JOIN Helpful
        ON productRatings.reviewer = Helpful.reviewer AND productRatings.reviewee = Helpful.reviewee 
        WHERE productRatings.reviewer = :reviewer
        ORDER BY dateAndTime DESC
        LIMIT 10
        OFFSET :start
        ''', reviewer=reviewer, start=start)

        if rows is not None:
            return [Rating(*row) for row in rows]
        
        return None
    
    def s_ratings_from_user(reviewer, start):
        rows = app.db.execute('''
        SELECT *
        FROM sellerRatings
        WHERE reviewer = :reviewer
        ORDER BY dateAndTime DESC
        LIMIT 10
        OFFSET :start
        ''', reviewer=reviewer, start=start)

        if rows is not None:
            return [Rating(*row) for row in rows] 
        
        return None

    @staticmethod #Get all ratings written about a reviewee from given table
    def other_product_ratings(reviewee, start, reviewer=None):
        if reviewer is not None:
            rows = app.db.execute('''
            WITH Helpful(reviewer, reviewee, score) AS (SELECT reviewer, reviewee, sum(action) FROM productRatingsReactions GROUP BY reviewer, reviewee)

            SELECT productRatings.reviewer, productRatings.reviewee, productRatings.rating, productRatings.review, productRatings.dateAndTime, Helpful.score
            FROM productRatings LEFT OUTER JOIN Helpful
            ON productRatings.reviewer = Helpful.reviewer AND productRatings.reviewee = Helpful.reviewee 
            WHERE productRatings.reviewer != :reviewer AND productRatings.reviewee = :reviewee
            ORDER BY dateAndTime DESC
            LIMIT 10
            OFFSET :start
            ''', reviewee=reviewee, reviewer=reviewer, start=start)
        else:
            rows = app.db.execute('''
            WITH Helpful(reviewer, reviewee, score) AS (SELECT reviewer, reviewee, sum(action) FROM productRatingsReactions GROUP BY reviewer, reviewee)

            SELECT productRatings.reviewer, productRatings.reviewee, productRatings.rating, productRatings.review, productRatings.dateAndTime, Helpful.score
            FROM productRatings LEFT OUTER JOIN Helpful
            ON productRatings.reviewer = Helpful.reviewer AND productRatings.reviewee = Helpful.reviewee 
            WHERE productRatings.reviewee = :reviewee
            ORDER BY dateAndTime DESC
            LIMIT 10
            OFFSET :start
            ''', reviewee=reviewee, start=start)
        
        if rows is not None:
            return [Rating(*row) for row in rows] 
        
        return None

    @staticmethod #Get all ratings written about a reviewee from given table
    def other_seller_ratings(reviewee, start, reviewer=None):
        if reviewer is not None:
            rows = app.db.execute('''
            SELECT *
            FROM sellerRatings
            WHERE reviewee = :reviewee AND reviewer != :reviewer
            ORDER BY dateAndTime DESC
            LIMIT 10
            OFFSET :start
            ''', reviewee=reviewee, reviewer=reviewer, start=start)
        else:
            rows = app.db.execute('''
            SELECT *
            FROM sellerRatings
            WHERE reviewee = :reviewee
            ORDER BY dateAndTime DESC
            LIMIT 10
            OFFSET :start
            ''', reviewee=reviewee, start=start)

        if rows is not None:
            return [Rating(*row) for row in rows] 
        
        return None

    #Get product review written by a user
    @staticmethod
    def get_your_p_review(reviewer, reviewee):  
        rows = app.db.execute('''
        WITH Helpful(reviewer, reviewee, score) AS (SELECT reviewer, reviewee, sum(action) FROM productRatingsReactions GROUP BY reviewer, reviewee)

        SELECT productRatings.reviewer, productRatings.reviewee, productRatings.rating, productRatings.review, productRatings.dateAndTime, Helpful.score
        FROM productRatings LEFT OUTER JOIN Helpful
        ON productRatings.reviewer = Helpful.reviewer AND productRatings.reviewee = Helpful.reviewee 
        WHERE productRatings.reviewer = :reviewer AND productRatings.reviewee = :reviewee
        ''', reviewer=reviewer, reviewee=reviewee)
        
        if rows is not None and bool(rows):
            return Rating(*(rows[0]))  
        else:
            return None

    #Get seller review written by a user
    @staticmethod
    def get_your_s_review(reviewer, reviewee):
        rows = app.db.execute('''
        SELECT * from sellerRatings
        WHERE reviewer = :reviewer AND reviewee = :reviewee
        ''', reviewer=reviewer, reviewee=reviewee)

        if rows is not None and bool(rows):
            return Rating(*(rows[0]))  
        else:
            return None

    #Obtain summary info about product or seller ratings
    @staticmethod
    def product_summary(reviewee):
        rows = app.db.execute('''
        SELECT count(reviewee), avg(rating)
        FROM productRatings
        WHERE reviewee = :reviewee
        ''', reviewee=reviewee)

        if rows is not None and bool(rows):
            return rows[0][0], rows[0][1]
        else:
            return 0, "N/A"
    
    @staticmethod
    def seller_summary(reviewee):
        rows = app.db.execute('''
        SELECT count(reviewee), avg(rating)
        FROM sellerRatings
        WHERE reviewee = :reviewee
        ''', reviewee=reviewee)
    
        if rows is not None and bool(rows):
            return rows[0][0], rows[0][1]
        else:
            return 0, "N/A"
    
    #Add new rating
    @staticmethod
    def add_p_rating(reviewer, reviewee, rating, dateAndTime, review='', helpful=0):
        rows = app.db.execute('''
        INSERT INTO productRatings(reviewer, reviewee, rating, review, dateAndTime, helpful) 
        VALUES(:reviewer, :reviewee, :rating, :review, :dateAndTime, :helpful)
        RETURNING *
        ''',reviewer=reviewer, reviewee=reviewee, rating=rating, review=review, dateAndTime=dateAndTime, helpful=helpful)

        if rows is not None and bool(rows):
            return Rating(*(rows[0]))  
        else:
            return None
    
    @staticmethod
    def add_s_rating(reviewer, reviewee, rating, dateAndTime, review='', helpful=0):
        rows = app.db.execute('''
        INSERT INTO sellerRatings(reviewer, reviewee, rating, review, dateAndTime, helpful) 
        VALUES(:reviewer, :reviewee, :rating, :review, :dateAndTime, :helpful)
        RETURNING *
        ''',reviewer=reviewer, reviewee=reviewee, rating=rating, review=review, dateAndTime=dateAndTime, helpful=helpful)

        if rows is not None and bool(rows):
            return Rating(*(rows[0]))  
        else:
            return None
    
    #Update existing rating
    @staticmethod
    def update_product_rating(reviewer, reviewee, rating, review):
        rows = app.db.execute('''
        UPDATE productRatings SET rating = :rating, review = :review
        WHERE reviewer = :reviewer AND reviewee = :reviewee
        RETURNING *
        ''', rating=rating, review=review, reviewer=reviewer, reviewee=reviewee)

        if rows is not None and bool(rows):
            return Rating(*(rows[0]))  
        else:
            return None
    
    @staticmethod
    def update_seller_rating(reviewer, reviewee, rating, review):
        rows = app.db.execute('''
        UPDATE sellerRatings SET rating = :rating, review = :review
        WHERE reviewer = :reviewer AND reviewee = :reviewee
        RETURNING *
        ''', rating=rating, review=review, reviewer=reviewer, reviewee=reviewee)

        if rows is not None and bool(rows):
            return Rating(*(rows[0]))  
        else:
            return None
    
    #Delete existing rating
    @staticmethod
    def delete_product_rating(reviewer, reviewee):
        rows = app.db.execute('''
        DELETE FROM productRatings 
        WHERE reviewer = :reviewer AND reviewee = :reviewee
        RETURNING reviewer
        ''', reviewer=reviewer, reviewee=reviewee)

        if rows is not None:
            reviewer = rows[0][0]
            return reviewer
        
        return False

    @staticmethod
    def delete_seller_rating(reviewer, reviewee):
        rows = app.db.execute('''
        DELETE FROM sellerRatings 
        WHERE reviewer = :reviewer AND reviewee = :reviewee
        RETURNING reviewer
        ''', reviewer=reviewer, reviewee=reviewee)

        if rows is not None:
            reviewer = rows[0][0]
            return reviewer
        
        return False
    
    #Check if current user can review seller
    @staticmethod
    def can_review_seller(reviewer, reviewee):
        rows = app.db.execute('''
        SELECT * from OrderContents, Listing where OrderContents.l_id = Listing.l_id AND
        Listing.seller_id = :seller AND OrderContents.u_id = :user
        ''', seller=reviewee, user=reviewer)

        if rows is not None and bool(rows):
            return True

        return False
    
    #Get top 3 most upvoted reviews
    def get_top_p_reviews(reviewee):
        rows = app.db.execute('''
            WITH Helpful(reviewer, reviewee, score) AS (SELECT reviewer, reviewee, sum(action) FROM productRatingsReactions GROUP BY reviewer, reviewee)

            SELECT productRatings.reviewer, productRatings.reviewee, productRatings.rating, productRatings.review, productRatings.dateAndTime, Helpful.score
            FROM productRatings LEFT OUTER JOIN Helpful
            ON productRatings.reviewer = Helpful.reviewer AND productRatings.reviewee = Helpful.reviewee 
            WHERE productRatings.reviewee = :reviewee
            ORDER BY Helpful.score DESC NULLS LAST
            LIMIT 3
            ''', reviewee=reviewee)

        return [Rating(*row) for row in rows] 
    
    #Determine if user can upvote or downvote a review
    def can_like_p_review(reviewer, reviewee, liker, action):
        has_liked = app.db.execute('''
        SELECT * from productRatingsReactions
        WHERE reviewer = :reviewer AND reviewee = :reviewee AND liker = :liker
        ''', reviewer=reviewer, reviewee=reviewee, liker=liker)

        if has_liked is not None and bool(has_liked):
            update = 1
            prev_action = app.db.execute('''
            SELECT * from productRatingsReactions
            WHERE reviewer = :reviewer AND reviewee = :reviewee AND liker = :liker AND action = :action
            ''', reviewer=reviewer, reviewee=reviewee, liker=liker, action=action)

            if prev_action is None or not(bool(prev_action)):
                return True, update
            else:
                return False, -1

        else:
            update = 0
            return True, update

    #Upvote or downvote a review
    def like_p_review(reviewer, reviewee, liker, action, dateAndTime, update):
        if update == 0:
            rows = app.db.execute('''
            INSERT INTO productRatingsReactions(reviewer, reviewee, liker, action, dateAndTime) 
            VALUES(:reviewer, :reviewee, :liker, :action, :dateAndTime)
            RETURNING *
            ''', reviewer=reviewer, reviewee=reviewee, liker=liker, action=action, dateAndTime=dateAndTime)
        elif update == 1:
            rows = app.db.execute('''
            UPDATE productRatingsReactions SET action = :action
            WHERE reviewer = :reviewer AND reviewee = :reviewee AND liker = :liker
            RETURNING *
            ''', action=action, reviewer=reviewer, reviewee=reviewee, liker=liker)
        
        if rows is not None and bool(rows):
            return True
        
        return False
    
    #Undo an upvote or downvote
    def remove_p_review_like(reviewer, reviewee, liker):
        has_liked = app.db.execute('''
        SELECT * from productRatingsReactions
        WHERE reviewer = :reviewer AND reviewee = :reviewee AND liker = :liker
        ''', reviewer=reviewer, reviewee=reviewee, liker=liker)

        if has_liked is not None and bool(has_liked):
            rows = app.db.execute('''
            DELETE FROM productRatingsReactions 
            WHERE reviewer = :reviewer AND reviewee = :reviewee AND liker = :liker
            RETURNING *
            ''', reviewer=reviewer, reviewee=reviewee, liker=liker)

            if rows is not None and bool(rows):
                return True
        
        return False
    
class Message:
    def __init__(self, order, author, listing, message, dateAndTime):
        self.order = order
        self.author = author
        self.listing = listing
        self.message = message
        self.dateAndTime = dateAndTime
    
    #Display all messages in a thread
    def get_messages(order, listing):
        rows = app.db.execute('''
        SELECT * FROM messages
        WHERE assoc_order = :order AND assoc_listing = :listing
        ORDER BY dateAndTime DESC
        ''', order=order, listing=listing)

        if rows is not None and bool(rows):
            return [Message(*row) for row in rows]
        else:
            return None

    #Add a new message
    def add_message(order, author, listing, message, dateAndTime):
        rows = app.db.execute('''
        INSERT INTO messages(assoc_order, author, assoc_listing, message, dateAndTime) 
        VALUES(:order, :author, :listing, :message, :dateAndTime)
        RETURNING *
        ''', order=order, author=author, listing=listing, message=message, dateAndTime=dateAndTime) 

        if rows is not None and bool(rows):
            return Message(*(rows[0]))  
        else:
            return None


    

    
