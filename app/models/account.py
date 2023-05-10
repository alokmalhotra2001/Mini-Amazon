from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

class Account:
    def __init__(self, id, firstname, lastname, address, email, balance, password) -> None:
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.balance = balance
        self.password = password
    
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

    #adds user to the seller DB and hence gives them seller capabilities
    def become_seller(id):
        try:
            app.db.execute('''
        INSERT INTO Sellers (id) VALUES
        (:id)
        ''', id=id)
            return
        except Exception:
            #Balance.make_card(id, amount)
            return

    #pulls demographic info of the user
    def get_info(id):
        rows = app.db.execute('''
            SELECT id, firstname, lastname, address, email, balance, password
            FROM Users
            WHERE id = :id
            ''',
                                    id=id)
        
        return Account(*(rows[0])) if rows else None
    
    #Updates the first name of the user
    def update_first(id, first):
        rows = app.db.execute('''
    UPDATE Users
    SET firstname = :first
    WHERE id = :id
    RETURNING *
    ''',  id=id, first=first)
        return Account.get_info(id)
    
    #Updates the last name of the user
    def update_last(id, last):
        rows = app.db.execute('''
    UPDATE Users
    SET lastname = :last
    WHERE id = :id
    RETURNING *
    ''',  id=id, last=last)
        return Account.get_info(id)
    
    #Updates address
    def update_address(id, address):
        rows = app.db.execute('''
    UPDATE Users
    SET address = :address
    WHERE id = :id
    RETURNING *
    ''',  id=id, address=address)
        return Account.get_info(id)
    
    #Updates password
    def update_password(id, password):
        rows = app.db.execute('''
    UPDATE Users
    SET password = :password
    WHERE id = :id
    RETURNING *
    ''',  id=id, password=generate_password_hash(password))
        return Account.get_info(id)
    
    #Update emails, if an account already exists 
    def update_email(id, email):
        #WORK IN PROGRESS, making sure emails unique
        rows = app.db.execute('''
            SELECT id, firstname, lastname, address, email, balance, password
            FROM Users
            WHERE email = :email
            ''',
                                    email=email)
        if rows is not None and bool(rows):
            print("An account with this email address is already in use. Please choose another.")
            ##ADD FLASK ALERT
            return Account.get_info(id)
        #Need to fix else statement
        else:
            
            rows = app.db.execute('''
        UPDATE Users
        SET email = :email
        WHERE id = :id
        RETURNING *
        ''',  id=id, email=email)
            return Account.get_info(id)
