from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, price, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.price = price
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, price, time_purchased
FROM Listing
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, price, time_purchased
FROM Listing
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
