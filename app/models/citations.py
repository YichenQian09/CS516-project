from flask import current_app as app
from .paper import Paper


class Citations:
    def __init__(self, uid):
        self.uid = uid

    @staticmethod
    def get_citations(uid):
        rows = app.db.execute(
            '''
            SELECT pid, title, year, conference
            FROM Papers
            WHERE pid IN (
                SELECT cite_pid
                FROM Users_cite_history
                WHERE uid = :uid
            )
            ORDER BY pid
            '''
        , uid = uid)
        return [Paper(*row) for row in rows]

        