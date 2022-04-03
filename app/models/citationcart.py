from flask import current_app as app
from .paper import Paper


class CitationCart:
    def __init__(self, uid, cite_pid, time_added):
        self.uid = uid
        self.cite_pid = cite_pid
        self.time_added=time_added
    
    @staticmethod
    def get_each_citation_cart(uid):
        #Returns a list of papers
        rows=app.db.execute(
            '''
            SELECT User_cart.cite_pid AS pid, Papers.title as title, Papers.year as year, Papers.conference as conference
            FROM User_cart, Papers
            WHERE User_cart.uid = :uid AND User_cart.cite_pid=Papers.pid
            ''', uid=uid)
        return [Paper(*row) for row in rows]

    @staticmethod
    def check_if_already_in_cart(uid,pid):
        rows = app.db.execute('''
        SELECT count(*)
        FROM user_cart
        WHERE uid =:uid AND cite_pid =:pid
        ''', uid= uid, pid = pid)
        return True if rows is not None and rows[0][0]>0 else False

    @staticmethod
    def add_paper_to_cart(uid,pid):
        rows = app.db.execute('''
            INSERT INTO user_cart(uid, cite_pid, time_added )
            VALUES(:uid, :pid, current_timestamp)
            RETURNING cite_pid
            ''',
                              uid=uid,pid=pid)
        print(rows)
        return rows[0][0] if rows is not None else None
