from flask import current_app as app

class History:
    #def __init__(self, id, buyer_id, placed, fulfilled, num_items) -> None:
    def __init__(self, id, placed, fulfilled, num_items) -> None:
        self.id = id
        #self.buyer_id = buyer_id
        self.placed = placed
        self.fulfilled = fulfilled
        self.num_items = num_items
    
    @staticmethod
    def get_history(buyer_id):
        print(buyer_id)
        rows = app.db.execute('''
    SELECT id, placed, fulfilled, num_items
    FROM Orders
    WHERE buyer_id = :buyer_id
    ORDER BY placed DESC
    ''', buyer_id=buyer_id)
    #make sure to revert id back to buyer_id
        print([History(*row) for row in rows])
        return [History(*row) for row in rows]
        #return History(*(rows[0])) if rows else None
