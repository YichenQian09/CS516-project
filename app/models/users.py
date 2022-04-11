from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Users(UserMixin):
    def __init__(self, uid, nickname, citenum, research_interest):
        self.uid = uid
        self.nickname = nickname
        self.citenum = citenum
        self.research_interest = research_interest

    @staticmethod
    def get_profile(uid):
        rows = app.db.execute("""
SELECT uid, nickname, citenum, research_interest
FROM Users
WHERE uid = :uid
""",
                              uid=uid)
        print(not rows)
        if not rows:  # user not found
            return None
        else:
            return Users(*(rows[0]))
    
    @staticmethod
    def update_nickname(uid,nickname):
        rows = app.db.execute("""
UPDATE users
SET nickname =:nickname
WHERE uid = :uid
""",
                              uid=uid,nickname=nickname)
        return rows if rows is not None else None