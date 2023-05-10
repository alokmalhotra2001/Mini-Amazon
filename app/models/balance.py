from flask import current_app as app
import string
import random

class Balance:
    def __init__(self, id, balance) -> None:
        self.id = id
        self.balance = balance
    
    # Simple function that gets the balance of the user
    @staticmethod    
    def get_balance(id):
        
        rows = app.db.execute('''
    SELECT id, balance
    FROM Users
    WHERE id = :id
    ''',
                            id=id)
        return Balance(*(rows[0])) if rows else None
    
    # Updates balance based off passed in withdrawal or deposit amount
    def update_balance(id, amount):
        rows = app.db.execute('''
    UPDATE Users
    SET balance = balance + :amount
    WHERE id = :id
    RETURNING *
    ''',  id=id, amount=amount)
        
        return Balance.get_balance(id)

    # If a gift card is valid, changes used bit to 1 to ensure that the card cannot be used again
    # Also calls update balance to actually increment the user's balance
    def use_card(id, code, amount):
        rows = app.db.execute('''
    UPDATE Gift
    SET used = 1
    WHERE code = :code
    RETURNING *
    ''',  id=id, code=code, amount=amount)
        return Balance.update_balance(id, amount)

    # Checks to see if the code is valid. If so, uses the card.
    def verify_code(id, code):
        rows = app.db.execute('''
    SELECT amount
    FROM Gift
    WHERE code = :code and used = 0
    ''',
                            code=code)
        if rows is not None and bool(rows):
            return Balance.use_card(id, code, rows[0][0])
        else:
            print("code invalid")
            return None

    def generate_code():
        #Generates a random integer for code generation
        return random.randint(1000000000, 2000000000)
    
    # tricky try-catch, ensures validity of code
    def make_card(id, amount):
        #make unique 10 digit code for card -- FOR FUTURE: Introduce longer, more secure length
        code = Balance.generate_code()
        print(amount)
        # On the (extremely rare) chance that a code already exists in the DB, ensures the insert runs smoothly
        try:
            app.db.execute('''
        INSERT INTO Gift (code, amount, used) VALUES
        (:code, :amount, 0)
        ''', code=code, amount=amount)
            return Balance.get_balance(id)
        except Exception:
            #Balance.make_card(id, amount)
            return amount, code, Balance.update_balance(id, -1*(float(amount)))
