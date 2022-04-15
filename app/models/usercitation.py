from flask import current_app as app
from .paper import Paper

class Usercitation:
    def __init__(self, uid, order_num, cite_pid):
        self.uid = uid
        self.order_num = order_num
        self.cite_pid = cite_pid

    @staticmethod
    def add_to_usercitation(uid, order_num, cite_pids):
        for cite_pid in cite_pids:
            app.db.execute(
                '''
                INSERT INTO Users_cite_history (uid, order_num, cite_pid)
                VALUES(:uid, :order_num, :cite_pid)
                ''', uid=uid, order_num=order_num, cite_pid=cite_pid
            )

    @staticmethod
    def get_user_citation_records(uid):
        rows = app.db.execute(
            '''
            SELECT pid, title,year, conference
            FROM papers
            WHERE pid IN (
                SELECT cite_pid FROM Users_cite_history WHERE uid = :uid
            ) 
            '''
        )
        return [Paper(*row) for row in rows]
        