from flask import current_app as app

class Abstract:
    def __init__(self, pid, abstract):
        self.pid = pid
        self.abstract = abstract

    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT pid, abstract
            FROM abstract
            WHERE pid = :pid
            ''', pid=pid)
        if len(rows) == 0:
            return None
        return Abstract(*(rows[0]))