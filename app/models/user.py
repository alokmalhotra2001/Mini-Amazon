from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    #def __init__(self, id, email, password, address, firstname, lastname, balance):
    def __init__(self, id, email, firstname, lastname):
        self.id = id
        self.email = email
        #self.password = password
        #self.address = address
        self.firstname = firstname
        self.lastname = lastname
        #self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname
FROM Users
WHERE email = :email
""",
        #rows = app.db.execute("""
#SELECT password, id, email, firstname, lastname
#FROM Users
#""",
                              email=email)
        if not rows:  # email not found
            print("Nothing found from database")
            return None
        elif not check_password_hash(rows[0][0], password) and not check_password_hash(generate_password_hash(rows[0][0]), password):
            # incorrect password
            print("Incorrect password")
            return None
        else:
            print(*(rows[0][1:]))
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, address, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, address, firstname, lastname, balance)
VALUES(:email, :password, :address, :firstname, :lastname, :balance)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  address=address,
                                  firstname=firstname,
                                  lastname=lastname,
                                  balance=0)
            id = rows[0][0]
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
