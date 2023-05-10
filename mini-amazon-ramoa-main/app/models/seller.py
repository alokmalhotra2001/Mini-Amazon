from flask import current_app as app

class Seller:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get_seller_name(id):
        rows = app.db.execute('''
SELECT firstname, lastname
FROM Users
WHERE id = :id
''',
                              id=id)
        return Users(*(rows[0])) if rows is not None else None
