from flask import current_app as app

class BuyerInfo:
    def __init__(self, id, firstname, lastname, address, email) -> None:
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        # self.balance = balance
        # print("Hello")
        # if seller, also grab email and address
    # gets information of a specific buyer
    def get_info(id):
        rows = app.db.execute('''
            SELECT id, firstname, lastname, address, email
            FROM Users
            WHERE id = :id
            ''',
                                    id=id)
        # print("got your account " + str(id))
        
        return BuyerInfo(*(rows[0])) if rows else None
