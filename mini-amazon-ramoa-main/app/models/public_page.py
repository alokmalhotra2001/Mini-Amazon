from flask import current_app as app

class PublicProfile:
    def __init__(self, id, firstname, lastname, address=0, email=0) -> None:
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        print("Hello")
        # if seller, also grab email and address

    def get_if_seller(id):
        # checks if this user is also a seller
        rows = app.db.execute('''
    SELECT id
    FROM Sellers
    WHERE id = :id
    ''',
                              id=id)
        if len(rows)<1:
            return False
        else:
            return True

    # Gets public profile information and provides more if someone is a seller
    @staticmethod    
    def get_info(id):
        #checks if user is seller
        seller = PublicProfile.get_if_seller(id)
        #if not a seller, only provide id, first name, and last name
        if seller == False:
            rows = app.db.execute('''
    SELECT id, firstname, lastname
    FROM Users
    WHERE id = :id
    ''',
                              id=id)
            return PublicProfile(*(rows[0])) if rows else None
        else:
            #if a seller, add address and email
            rows = app.db.execute('''
    SELECT id, firstname, lastname, address, email
    FROM Users
    WHERE id = :id
    ''',
                              id=id)
        return PublicProfile(*(rows[0])) if rows else None
        
