from flask import current_app as app

class Authors:
    def __init__(self, pid, author):
        self.pid = pid
        self.author = author

    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute(
            '''
            SELECT pid, author
            FROM authorship
            WHERE pid = :pid
            ''', pid=pid)
        return [Authors(*row) for row in rows]
    
    def get_pid_by_author(author):
        rows = app.db.execute(
            '''
            SELECT pid, author
            FROM authorship
            WHERE author =:author
            ''', author=author
        )
        return [Author(*row) for row in rows]