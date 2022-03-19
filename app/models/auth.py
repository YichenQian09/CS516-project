from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Auth(UserMixin):
    def __init__(self, uid, email, firstname, lastname, school):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.school = school
    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, uid, email, firstname, lastname, school
FROM Auth
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return Auth(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Auth
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, school):
        try:
            rows = app.db.execute("""
INSERT INTO Auth(email, password, firstname, lastname, school)
VALUES(:email, :password, :firstname, :lastname, :school)
RETURNING uid
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, school=school)
            uid = rows[0][0]
            return Auth.get(uid)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute("""
SELECT uid, email, firstname, lastname, school
FROM Auth
WHERE uid = :uid
""",
                              uid=uid)
        return Auth(*(rows[0])) if rows else None
    # override the get_id function
    def get_id(self):
        return (self.uid)
    
    def get_email(self):
        return (self.email)

    # update auth information
    @staticmethod
    def update(auth, email, password, firstname, lastname, school):
        uid=auth.uid
        try:
            rows = app.db.execute("""
    update Auth
    set email=:email, password=:password, firstname=:firstname, lastname=:lastname, school=:school 
    WHERE uid = :uid
    """,
                                    email=email,
                                    password=generate_password_hash(password),
                                    firstname=firstname, lastname=lastname, school=school,uid=uid)
            return Auth(*(rows[0])) if rows else None
        except Exception as e:
                # likely email already in use; better error checking and reporting needed;
                # the following simply prints the error to the console:
            print(str(e))
            return None
