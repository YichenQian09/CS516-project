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
        print("profile:",rows)

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

    #set basic info when register
    @staticmethod
    def set_basic_info(uid,nickname,chosenInterests):
        interests=','.join(chosenInterests)
        rows = app.db.execute("""
insert into users(uid,nickname,citenum,research_interest)
values (:uid,:nickname,0,:interests)
""",
                              uid=uid,nickname=nickname,interests=interests)
        return rows if rows is not None else None

    # if the user register, then check if there is an existing email; 
    # if the user update, then check if there is an existing email except its own email
    @staticmethod
    def nickname_exists(nickname, uid=-1):
        rows = app.db.execute("""
SELECT nickname
FROM users
WHERE nickname = :nickname
AND uid <> :uid
""",
                              nickname=nickname,uid=uid)
        return len(rows) > 0
    
    #update nickname and research_interests
    @staticmethod
    def update_info(uid,nickname,chosenInterests):
        interests=','.join(chosenInterests)
        rows = app.db.execute("""
update users
set nickname =:nickname,
research_interest = :interests
WHERE uid = :uid
""",
                              uid=uid,nickname=nickname,interests=interests)
        return rows if rows is not None else None
    
    @staticmethod
    def get_info(uid):
        rows = app.db.execute("""
select nickname,research_interest
from users
WHERE uid = :uid
""",
                              uid=uid)
        if not rows[0]:
            return None
        interests_list=[]
        if rows[0][1]:
            interests_list=rows[0][1].split(',')
        return rows[0][0],interests_list

